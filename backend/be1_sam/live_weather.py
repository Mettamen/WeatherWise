"""Sam: bounded live requests, explicit source status and no synthetic fallback."""
import asyncio
import math
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import httpx
from shared.contracts import WeatherHour, Location, ScoredHour
from backend.be2_metta.service import build_dashboard
from backend.be2_metta.risk import evaluate
from backend.be2_metta.scheduler import best_windows
from backend.be2_metta.alerts import build_alerts

FORECAST = "https://api.open-meteo.com/v1/forecast"
AIR = "https://air-quality-api.open-meteo.com/v1/air-quality"
_cache = {}
FIELDS = "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m,is_day"

def heat_index(c, rh):
    """NWS simple estimate then Rothfusz regression when appropriate."""
    f = c * 9 / 5 + 32
    estimate = .5 * (f + 61 + (f - 68) * 1.2 + rh * .094)
    if (estimate + f) / 2 < 80:
        return round((estimate - 32) * 5 / 9, 1)
    h = (-42.379 + 2.04901523*f + 10.14333127*rh - .22475541*f*rh
         - .00683783*f*f - .05481717*rh*rh + .00122874*f*f*rh
         + .00085282*f*rh*rh - .00000199*f*f*rh*rh)
    if rh < 13 and 80 <= f <= 112:
        h -= (13-rh)/4 * math.sqrt((17-abs(f-95))/17)
    elif rh > 85 and 80 <= f <= 87:
        h += (rh-85)/10 * (87-f)/5
    return round((h-32)*5/9, 1)

def scene_for(w):
    code = w.weather_code or 0
    if code >= 95: return "storm"
    if code in {71,73,75,77,85,86}: return "snow"
    if w.rainfall_mm_hr > .1 or code in {51,53,55,56,57,61,63,65,66,67,80,81,82}: return "rain"
    if code in {45,48}: return "fog"
    if w.wind_kmh >= 25: return "wind"
    if (w.cloud_cover or 0) >= 70: return "cloudy"
    if not w.is_day: return "night"
    return "partly" if (w.cloud_cover or 0) > 20 else "sunny"

async def fetch_bundle(lat, lon):
    key = (round(lat, 2), round(lon, 2))
    existing = _cache.get(key)
    if existing and time.monotonic() - existing[0] < 600:
        return existing[1]
    common = dict(latitude=key[0], longitude=key[1], timezone="auto", forecast_days=2)
    async with httpx.AsyncClient(timeout=15, headers={"User-Agent":"WeatherWise-Prototype/1.1"}) as client:
        async def get(url, params):
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                if data.get("error"): return None
                return data
            except (httpx.HTTPError, ValueError): return None
        gfs, ecmwf, air = await asyncio.gather(
            get(FORECAST, common | dict(models="gfs_seamless", current=FIELDS, hourly=FIELDS+",uv_index")),
            get(FORECAST, common | dict(models="ecmwf_ifs025", current=FIELDS, hourly=FIELDS+",uv_index")),
            get(AIR, common | dict(hourly="pm2_5,us_aqi")),
        )
    result = (gfs, ecmwf, air, datetime.now(timezone.utc).isoformat())
    if len(_cache) >= 128: _cache.pop(next(iter(_cache)))
    if gfs or ecmwf: _cache[key] = (time.monotonic(), result)
    return result

def valid_model(payload, now):
    try:
        zone = ZoneInfo(payload["timezone"])
        at = datetime.fromisoformat(payload["current"]["time"]).replace(tzinfo=zone)
        age = (now-at).total_seconds()
        return -3600 <= age <= 10800 and all(payload["current"].get(k) is not None for k in ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"])
    except (TypeError, KeyError, ValueError): return False

def assemble_live(profile, repo, lat, lon, bundle, now=None):
    now = now or datetime.now(timezone.utc)
    gfs, ecmwf, air, fetched = bundle
    models = [("NOAA GFS", gfs), ("ECMWF IFS", ecmwf)]
    valid = [(name,payload) for name,payload in models if valid_model(payload, now)]
    if not valid: raise ValueError("Live weather is unavailable or older than 3 hours. Retry, or explicitly switch to sample data.")
    primary_name, primary = valid[0]
    tz = ZoneInfo(primary["timezone"])
    local_now = now.astimezone(tz)
    date = local_now.date().isoformat()
    hourly = primary["hourly"]
    air_rows = {}
    if air and "hourly" in air:
        air_rows = {t: {key: air["hourly"].get(key, [None]*len(air["hourly"]["time"]))[i] for key in ["pm2_5", "us_aqi"]} for i,t in enumerate(air["hourly"]["time"])}
    def make(raw):
        t = raw["time"]
        a = air_rows.get(t[:13]+":00", {})
        temp, rh = raw.get("temperature_2m"), raw.get("relative_humidity_2m")
        if temp is None or rh is None or raw.get("wind_speed_10m") is None or raw.get("precipitation") is None:
            return None
        return WeatherHour(timestamp=datetime.fromisoformat(t).replace(tzinfo=tz).isoformat(),
            temperature_c=temp, relative_humidity_pct=rh, heat_index_c=heat_index(temp,rh),
            rainfall_mm_hr=raw["precipitation"], aqi=round(a["us_aqi"]) if a.get("us_aqi") is not None else None,
            pm2_5_ugm3=a.get("pm2_5"), uv_index=raw.get("uv_index"), wind_kmh=raw["wind_speed_10m"],
            weather_code=raw.get("weather_code"), cloud_cover=raw.get("cloud_cover"), is_day=bool(raw.get("is_day", 1)),
            apparent_temperature_c=raw.get("apparent_temperature"))
    weather = []
    for i,t in enumerate(hourly["time"]):
        if t[:10] == date:
            w = make({k:values[i] for k,values in hourly.items()})
            if w: weather.append(w)
    if not weather: raise ValueError("The provider returned no usable hourly data for today.")
    raw_current = dict(primary["current"])
    matching = next((w for w in weather if w.timestamp[:13] == raw_current["time"][:13]), None)
    raw_current["uv_index"] = matching.uv_index if matching else None
    current = make(raw_current)
    if current is None: raise ValueError("Current weather measurements are incomplete.")
    result = build_dashboard(profile, Location(location_id="LIVE", city="Your approximate area", state=""), weather, repo.conditions, repo.occupations[profile.occupation_id], date)
    result.focus_hour = ScoredHour(weather=current, risk=evaluate(current,profile,repo.conditions,repo.occupations[profile.occupation_id]))
    future = [h for h in result.hours if datetime.fromisoformat(h.weather.timestamp) >= local_now]
    result.daily_risk = max([result.focus_hour]+future, key=lambda h:h.risk.score).risk
    result.best_windows = best_windows(future,profile)
    result.alerts = build_alerts([result.focus_hour]+future,"LIVE")
    result.mode = "live"
    result.timezone = primary["timezone"]
    result.fetched_at = fetched
    result.valid_at = current.timestamp
    result.scene = scene_for(current)
    result.source = f"{primary_name} forecast model via Open-Meteo; air quality from CAMS via Open-Meteo"
    result.location_note = "Coordinates rounded to 0.01 degrees before provider requests; no health profile is shared."
    result.sources = [{"name": name+" via Open-Meteo", "status":"available" if (name,payload) in valid else "unavailable or stale", "valid_at":payload.get("current",{}).get("time") if payload else None, "url":"https://open-meteo.com/en/docs", "temperature_c":payload.get("current",{}).get("temperature_2m") if (name,payload) in valid else None} for name,payload in models]
    result.sources.append({"name":"CAMS air quality via Open-Meteo", "status":"available" if current.aqi is not None else "unavailable", "url":"https://open-meteo.com/en/docs/air-quality-api"})
    if len(valid)==2 and gfs["current"]["time"] == ecmwf["current"]["time"]:
        delta = round(abs(gfs["current"]["temperature_2m"]-ecmwf["current"]["temperature_2m"]),1)
        rain_agree = (gfs["current"]["precipitation"] > .1) == (ecmwf["current"]["precipitation"] > .1)
        result.comparison = {"status":"models agree closely" if delta <= 3 and rain_agree else "models disagree", "temperature_spread_c":delta,
            "message":f"Same-time temperature spread: {delta}°C. Rain signals {'agree' if rain_agree else 'differ'}. Comparison uses a 3°C demo tolerance, not an accuracy guarantee."}
    else:
        result.comparison = {"status":"comparison incomplete", "message":"A second same-time model estimate is unavailable. Weather has not been independently verified."}
    result.limitations = ["Model estimates, not local station observations or a view of the actual sky. Both models share Open-Meteo as the delivery service.",
        "Not all viable sources can be checked. Source agreement is not verification of ground truth.",
        "Risk uses illustrative rules. Disease transmission and stroke probability are not predicted.",
        "Current precipitation is a model-interval value; hourly chart rainfall is the preceding-hour accumulation.",
        "Only future complete windows remaining today are recommended; missing AQI or UV reduces scoring coverage."]
    return result
