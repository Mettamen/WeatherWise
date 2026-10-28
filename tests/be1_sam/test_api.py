"""Sam: API access, validation, isolation and data loading tests."""
def test_health_and_catalog(client):
    assert client.get("/api/v1/health").json()["mode"] == "synthetic_demo"
    catalog = client.get("/api/v1/catalog").json()
    assert len(catalog["locations"]) == 10
    assert len(catalog["conditions"]) == 15
    assert len(catalog["dates"]) == 28

def test_requires_session(client):
    assert client.get("/api/v1/dashboard").status_code == 401

def test_profiles_isolated_and_deleted(client, auth):
    profile = client.get("/api/v1/profile", headers=auth).json()
    profile["display_name"] = "Metta demo"
    assert client.put("/api/v1/profile", headers=auth, json=profile).status_code == 200
    second = client.post("/api/v1/sessions").json()
    assert second["profile"]["display_name"] == "Alex"
    assert client.get("/api/v1/profile", headers=auth).json()["display_name"] == "Metta demo"
    assert client.delete("/api/v1/session", headers=auth).status_code == 204
    assert client.get("/api/v1/profile", headers=auth).status_code == 401

def test_reject_unknown_reference_and_invalid_window(client, auth):
    profile = client.get("/api/v1/profile", headers=auth).json()
    profile["condition_ids"] = ["NOT_A_CONDITION"]
    assert client.put("/api/v1/profile", headers=auth, json=profile).status_code == 422
    profile["condition_ids"] = []
    profile.update(available_from=20, available_until=18)
    assert client.put("/api/v1/profile", headers=auth, json=profile).status_code == 422
    assert client.get("/api/v1/dashboard?date=2025-01-01", headers=auth).status_code == 404

def test_personal_response_not_cached(client, auth):
    assert client.get("/api/v1/profile", headers=auth).headers["cache-control"] == "no-store"

def test_root_is_frontend(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "WeatherWise" in response.text
    assert client.get("/js/app.js").status_code == 200
