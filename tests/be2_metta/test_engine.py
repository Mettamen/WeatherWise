"""Metta: boundaries, ranking feasibility, missing data and repeatability."""
from datetime import datetime, timedelta
import pytest
from shared.contracts import Profile, WeatherHour, ScoredHour, RiskResult
from backend.be2_metta.risk import evaluate, risk_level
from backend.be2_metta.scheduler import best_windows
from backend.be2_metta.alerts import build_alerts

def weather(**changes):
    return WeatherHour(**dict(timestamp="2026-05-08T12:00:00+05:30", temperature_c=27, relative_humidity_pct=50, heat_index_c=28, rainfall_mm_hr=0, aqi=40, uv_index=3, wind_kmh=5) | changes)

@pytest.mark.parametrize("score,level", [(0,"Low"),(24.9,"Low"),(25,"Moderate"),(49.9,"Moderate"),(50,"High"),(74.9,"High"),(75,"Severe"),(100,"Severe")])
def test_band_boundaries(score, level):
    assert risk_level(score) == level

def test_no_hazard_does_not_default_to_heat(repository):
    result = evaluate(weather(), Profile(), repository.conditions, repository.occupations["O08"])
    assert result.score == 0 and result.dominant_hazard == "none"

def test_profile_sensitivity_and_extreme_heat(repository):
    w = weather(heat_index_c=43)
    basic = evaluate(w, Profile(), repository.conditions, repository.occupations["O08"])
    sensitive = evaluate(w, Profile(age=70, condition_ids=["C03"]), repository.conditions, repository.occupations["O08"])
    assert sensitive.score > basic.score
    assert evaluate(weather(heat_index_c=80), Profile(), repository.conditions, repository.occupations["O08"]).score == 100

def scored_hours(scores):
    return [ScoredHour(weather=weather(timestamp=f"2026-05-08T{i:02}:00:00+05:30"), risk=RiskResult(score=score, level=risk_level(score), dominant_hazard="heat" if score else "none", reasons=["test"], advice=["test"])) for i, score in enumerate(scores)]

def test_scheduler_whole_activity_available_and_nonoverlapping():
    hours = scored_hours([5]*6 + [40,50,30,20,10,15,30,60,70,60,40,30,20,10,5,5,5,5])
    profile = Profile(available_from=9, available_until=18, activity_duration_hours=2)
    windows = best_windows(hours, profile)
    assert len(windows) == 3
    assert windows[0].start[11:13] == "10"
    for w in windows:
        start, end = datetime.fromisoformat(w.start), datetime.fromisoformat(w.end)
        assert start.hour >= 9 and end.hour <= 18
        assert end-start == timedelta(hours=2)
    for a, b in zip(sorted(windows, key=lambda w: w.start), sorted(windows, key=lambda w: w.start)[1:]):
        assert a.end <= b.start

def test_scheduler_does_not_bridge_missing_hours():
    hours = scored_hours([0]*24)
    hours.pop(10)
    windows = best_windows(hours, Profile(available_from=9, available_until=12, activity_duration_hours=2))
    assert windows == []

def test_alerts_group_consecutive_hours_and_are_stable():
    hours = scored_hours([0]*9 + [30,40,60] + [0]*12)
    alerts = build_alerts(hours, "LOC01")
    assert len(alerts) == 1
    assert alerts[0].window_start[11:13] == "09"
    assert alerts[0].window_end[11:13] == "12"
    assert alerts[0].severity == "High"
    assert alerts == build_alerts(hours, "LOC01")
