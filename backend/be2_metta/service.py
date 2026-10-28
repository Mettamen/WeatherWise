"""Metta's integration entry point. Sam supplies validated data and profile."""
from shared.contracts import Dashboard, Location, Profile, WeatherHour, ScoredHour
from .risk import evaluate
from .scheduler import best_windows
from .alerts import build_alerts

def build_dashboard(profile: Profile, location: Location, weather: list[WeatherHour], conditions: dict, occupation: dict, date: str) -> Dashboard:
    if not weather:
        raise ValueError("No weather is available for this date")
    hours = [ScoredHour(weather=w, risk=evaluate(w, profile, conditions, occupation)) for w in weather]
    peak = max(hours, key=lambda h: h.risk.score)
    focus = next((h for h in hours if h.weather.timestamp[11:13] == "12"), hours[0])
    return Dashboard(date=date, location=location, profile=profile, focus_hour=focus,
        daily_risk=peak.risk, hours=hours, best_windows=best_windows(hours, profile),
        alerts=build_alerts(hours, location.location_id), limitations=[
            "Synthetic weather and illustrative rules. No clinical or real-world prediction claims.",
            "Daily risk is the peak hourly score. The weather card shows 12:00 local time.",
            "Communicable-disease risk, road-level routing and real notifications are not implemented.",
        ])
