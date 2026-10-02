def test_health_envelope(client):
  response = client.get("/api/health")
  assert response.status_code == 200
  body = response.json()
  assert body["success"] is True
  assert body["code"] == 200
  assert body["data"] == {"status": "ok"}
