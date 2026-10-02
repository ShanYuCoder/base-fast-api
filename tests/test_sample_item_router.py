from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_sample_item_search_envelope():
  response = client.get("/api/sample-items")
  assert response.status_code == 200
  body = response.json()
  assert body["success"] is True
  assert "items" in body["data"]