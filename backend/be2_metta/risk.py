"""Metta: transparent demonstration rules; not a clinical risk model.

See docs/RISK_MODEL.md for formula and limits. No database/HTTP dependencies.
"""
from shared.contracts import Profile, WeatherHour, RiskResult

def risk_level(score: float) -> str:
    if score >= 75:
        return "Severe"
    if score >= 50:
        return "High"
    if score >= 25:
        return "Moderate"
    return "Low"

def evaluate(weather: WeatherHour, profile: Profile, conditions: dict, occupation: dict) -> RiskResult:
    selected = [conditions[c] for c in profile.condition_ids]
    heat_sensitivity = max([float(c["heat_sensitivity"]) for c in selected], default=0)
    air_sensitivity = max([float(c["air_quality_sensitivity"]) for c in selected], default=0)
    exposure = float(occupation["outdoor_exposure_fraction"])
    age_factor = 0.15 if profile.age >= 65 else 0
    components = {
        "heat": max(0, weather.heat_index_c - 30) * 3 * (1 + .45 * heat_sensitivity + .2 * exposure + age_factor),
        "rain": max(0, weather.rainfall_mm_hr - 2.5) * 2.5,
        "air_quality": max(0, (weather.aqi or 0) - 100) * .35 * (1 + .5 * air_sensitivity),
        "uv": max(0, (weather.uv_index or 0) - 5) * 5,
    }
    dominant = max(components, key=components.get)
    maximum = components[dominant]
    score = round(min(100, maximum + .15 * (sum(components.values()) - maximum)), 1)
    if not maximum:
        dominant = "none"
    reasons, advice = [], []
    if components["heat"]:
        reasons.append(f"Heat index is {weather.heat_index_c:.1f}°C; the demo heat threshold is 30°C.")
        advice.append("Consider cooler hours and shaded breaks for outdoor activities.")
        if heat_sensitivity:
            reasons.append("Your selected profile increases the illustrative heat sensitivity.")
        if {"C03", "C06"}.intersection(profile.condition_ids):
            advice.append("Follow your clinician's existing fluid plan; this demo does not set a hydration target.")
    if components["rain"]:
        reasons.append(f"Rainfall is {weather.rainfall_mm_hr:.1f} mm/hour.")
        advice.append("Check local travel advisories before leaving; road flooding is not measured here.")
    if components["air_quality"]:
        reasons.append(f"Synthetic AQI is {weather.aqi}; the demo threshold is 100.")
        advice.append("Consider reducing outdoor exposure when local air-quality advisories recommend it.")
    if components["uv"]:
        reasons.append(f"UV index is {weather.uv_index:.1f}.")
        advice.append("Plan shade and sun protection for outdoor time.")
    if not reasons:
        reasons = ["No configured demo hazard threshold is exceeded in this hour."]
        advice = ["Review conditions again before an outdoor activity; a low score is not a safety guarantee."]
    if weather.aqi is None or weather.uv_index is None:
        reasons.append("Incomplete inputs: unavailable AQI/UV are excluded; a low result may underestimate risk.")
    if profile.infectious_condition_ids:
        reasons.append("Communicable conditions are recorded, but transmission and disease-specific risk are not calculated.")
    return RiskResult(score=score, level=risk_level(score), dominant_hazard=dominant, reasons=reasons, advice=advice)
