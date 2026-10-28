"""Sam owns application composition and every HTTP route."""
import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from shared.contracts import Catalog, Dashboard, Profile, Session, Location, Coordinates
from backend.be2_metta.service import build_dashboard
from .repository import DatasetRepository, ROOT
from .storage import ProfileStore
from .live_weather import fetch_bundle, assemble_live
from .food import nearby_places, meal_ideas

bearer = HTTPBearer(auto_error=False)

def create_app(database_path: Path | None = None, repository: DatasetRepository | None = None):
    @asynccontextmanager
    async def lifespan(app):
        app.state.repo = repository or DatasetRepository()
        app.state.store = ProfileStore(database_path or Path(os.environ.get("WEATHERWISE_DB", str(ROOT / "runtime" / "weatherwise.sqlite3"))))
        yield

    app = FastAPI(title="WeatherWise demo API", version="1.0.0", lifespan=lifespan, docs_url=None, redoc_url=None,
        description="Local synthetic-data prototype. Anonymous sessions expire after 24 hours. Do not submit real health data.")

    @app.middleware("http")
    async def headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'"
        if request.url.path.startswith("/api"):
            response.headers["Cache-Control"] = "no-store"
        return response

    def authorized(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
        token = credentials.credentials if credentials else ""
        profile = app.state.store.get(token)
        if profile is None:
            raise HTTPException(401, "Demo session is missing or expired. Start a new demo.")
        return token, profile

    @app.get("/api/v1/health")
    def health():
        return {"status": "ok", "mode": "synthetic_demo", "schema_version": "1.0"}

    @app.get("/api/v1/catalog", response_model=Catalog)
    def catalog():
        return app.state.repo.catalog()

    @app.post("/api/v1/sessions", response_model=Session, status_code=201)
    def session():
        token, profile = app.state.store.create()
        return Session(token=token, profile=profile)

    @app.get("/api/v1/profile", response_model=Profile)
    def profile(auth=Depends(authorized)):
        return auth[1]

    @app.put("/api/v1/profile", response_model=Profile)
    def update_profile(profile: Profile, auth=Depends(authorized)):
        try:
            app.state.repo.validate_profile(profile)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        if not app.state.store.save(auth[0], profile):
            raise HTTPException(401, "Demo session expired")
        return profile

    @app.delete("/api/v1/session", status_code=204)
    def delete_session(auth=Depends(authorized)):
        app.state.store.delete(auth[0])
        return Response(status_code=204)

    @app.get("/api/v1/dashboard", response_model=Dashboard)
    def dashboard(date: str = "2026-05-08", auth=Depends(authorized)):
        profile = auth[1]
        repo = app.state.repo
        try:
            weather = repo.day(profile.home_location_id, date)
        except ValueError as exc:
            raise HTTPException(404, str(exc)) from exc
        return build_dashboard(profile, Location(**repo.locations[profile.home_location_id]), weather,
            repo.conditions, repo.occupations[profile.occupation_id], date)

    @app.post("/api/v1/live", response_model=Dashboard)
    async def live(coords: Coordinates, auth=Depends(authorized)):
        try:
            bundle = await fetch_bundle(coords.latitude, coords.longitude)
            return assemble_live(auth[1], app.state.repo, coords.latitude, coords.longitude, bundle)
        except (ValueError, KeyError, TypeError) as exc:
            raise HTTPException(503, "Live weather is unavailable or incomplete. Retry, or choose sample data explicitly.") from exc

    @app.get("/api/v1/food/ideas")
    def food_ideas(auth=Depends(authorized)):
        ideas, note = meal_ideas(auth[1])
        return {"ideas":ideas,"note":note,"guidance_url":"https://www.food.gov.uk/print/pdf/node/22196"}

    @app.post("/api/v1/food/nearby")
    async def food_nearby(coords: Coordinates, auth=Depends(authorized)):
        return await nearby_places(coords.latitude,coords.longitude)

    app.mount("/", StaticFiles(directory=ROOT / "frontend_shreshta", html=True), name="frontend")
    return app

app = create_app()
