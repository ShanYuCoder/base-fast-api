from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_workforce_check_in_envelope():
    response = client.post(
        "/api/workforce/check-in",
        json={"badge_id": "BADGE-001", "station_id": "ST-1"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["checked_in"] is True
    assert "employee_name" in body["data"]
