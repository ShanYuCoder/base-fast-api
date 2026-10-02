from app.common.http.api_response import error, success


def test_success_envelope_shape():
  payload = success({"id": 1}, message="Retrieved successfully")
  assert payload["success"] is True
  assert payload["code"] == 200
  assert payload["message"] == "Retrieved successfully"
  assert payload["data"] == {"id": 1}
  assert "user_message" in payload
  assert "meta" in payload


def test_error_envelope_shape():
  payload = error(422, "Validation Error", "Invalid input", errors={"field": ["required"]})
  assert payload["success"] is False
  assert payload["code"] == 422
  assert payload["error"] == "Validation Error"
  assert payload["errors"] == {"field": ["required"]}


def test_knowledge_query_route(client):
  response = client.post("/api/knowledge/query", json={"query": "lockout procedure"})
  assert response.status_code == 200
  body = response.json()
  assert body["success"] is True
  assert "citations" in body["data"]
  assert len(body["data"]["citations"]) >= 1
