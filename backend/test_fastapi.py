from fastapi.testclient import TestClient
from backend.fastapi_app import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello World from Ingres Virtual Assistant"}

def test_test_endpoint():
    r = client.get("/test")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "Test endpoint" in data["message"]
