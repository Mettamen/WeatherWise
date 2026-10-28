"""Shared acceptance tests. Change these only with all owners' agreement."""
from shared.contracts import Dashboard

def test_full_contract_and_profile_change(client, auth):
    response = client.get("/api/v1/dashboard?date=2026-05-08", headers=auth)
    assert response.status_code == 200
    data = Dashboard.model_validate(response.json())
    assert len(data.hours) == 24
    assert data.focus_hour.weather.timestamp.endswith("+05:30")
    assert data.daily_risk.score == max(h.risk.score for h in data.hours)
    profile = data.profile.model_dump()
    profile.update(home_location_id="LOC02", condition_ids=["C04"], available_from=10, available_until=16, activity_duration_hours=2)
    assert client.put("/api/v1/profile", headers=auth, json=profile).status_code == 200
    result = client.get("/api/v1/dashboard?date=2026-11-08", headers=auth).json()
    assert result["location"]["city"] == "Coimbatore"
    assert result["profile"]["condition_ids"] == ["C04"]
    assert all(10 <= int(w["start"][11:13]) < int(w["end"][11:13]) <= 16 for w in result["best_windows"])

def test_all_cities_and_seasons(client, auth):
    catalog = client.get("/api/v1/catalog").json()
    profile = client.get("/api/v1/profile", headers=auth).json()
    for city in catalog["locations"]:
        profile["home_location_id"] = city["location_id"]
        client.put("/api/v1/profile", headers=auth, json=profile)
        for date in ["2026-05-08", "2026-11-08"]:
            data = Dashboard.model_validate(client.get(f"/api/v1/dashboard?date={date}", headers=auth).json())
            assert len(data.hours) == 24
            assert all(0 <= h.risk.score <= 100 for h in data.hours)
