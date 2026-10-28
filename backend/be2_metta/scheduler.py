"""Metta: rank whole, non-overlapping activity windows within availability."""
from datetime import datetime, timedelta
from shared.contracts import Profile, ScoredHour, TimeWindow
from .risk import risk_level

def best_windows(hours: list[ScoredHour], profile: Profile, limit: int = 3) -> list[TimeWindow]:
    candidates = []
    duration = profile.activity_duration_hours
    for index, hour in enumerate(hours):
        start = datetime.fromisoformat(hour.weather.timestamp)
        block = hours[index:index + duration]
        if len(block) != duration or start.hour < profile.available_from or start.hour + duration > profile.available_until:
            continue
        if any(datetime.fromisoformat(item.weather.timestamp) != start + timedelta(hours=i) for i, item in enumerate(block)):
            continue
        score = round(sum(item.risk.score for item in block) / duration, 1)
        candidates.append((score, start, start + timedelta(hours=duration)))
    chosen = []
    for score, start, end in sorted(candidates):
        if any(start < c[2] and c[1] < end for c in chosen):
            continue
        chosen.append((score, start, end))
        if len(chosen) == limit:
            break
    return [TimeWindow(start=start.isoformat(), end=end.isoformat(), average_score=score, level=risk_level(score),
        explanation=f"Lowest available {duration}-hour average scores within your chosen hours. This is a relative ranking, not a safe-time guarantee.")
        for score, start, end in chosen]
