import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# We assume the app will be created in src.main
# Since we are doing TDD, this import might fail if the file doesn't exist yet, 
# but for the "test first" philosophy, we define what we expect.
from main import app

client = TestClient(app)

API_KEY = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"
VALID_JWT = "random-jwt-token"

def test_health_check():
    """Requirement: /healthz must return 200"""
    response = client.get("/healthz")
    assert response.status_code == 200

def test_metrics_endpoint():
    """Requirement: /metrics must be exposed via prometheus"""
    response = client.get("/metrics")
    assert response.status_code == 200

def test_devops_post_success():
    """
    Requirement: 
    POST /DevOps with valid headers and payload.
    Returns: {"message": "Hello [to] your message will be send"}
    """
    payload = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }
    headers = {
        "X-Parse-REST-API-Key": API_KEY,
        "X-JWT-KWY": VALID_JWT
    }
    response = client.post("/DevOps", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Juan Perez your message will be send"}

def test_devops_unauthorized_no_headers():
    """Requirement: Missing headers should fail"""
    payload = {"message": "test", "to": "me", "from": "you", "timeToLifeSec": 10}
    response = client.post("/DevOps", json=payload)
    assert response.status_code in [401, 403]

def test_devops_unauthorized_invalid_apikey():
    """Requirement: Invalid API Key should fail"""
    payload = {"message": "test", "to": "me", "from": "you", "timeToLifeSec": 10}
    headers = {
        "X-Parse-REST-API-Key": "wrong-key",
        "X-JWT-KWY": VALID_JWT
    }
    response = client.post("/DevOps", json=payload, headers=headers)
    assert response.status_code in [401, 403]

def test_devops_invalid_method_get():
    """Requirement: Other HTTP Methods calls must return the string 'ERROR'"""
    headers = {
        "X-Parse-REST-API-Key": API_KEY,
        "X-JWT-KWY": VALID_JWT
    }
    response = client.get("/DevOps", headers=headers)
    # The requirement says "return string ERROR". 
    # Usually 405 Method Not Allowed is standard, but we must follow the strict req.
    # We will assume it returns 200 OK or 405 with "ERROR" body. 
    # Let's start by asserting the body contains ERROR.
    if response.headers.get("content-type") == "application/json":
        assert "ERROR" in str(response.content) or response.json() == "ERROR"
    else:
        assert response.text == "ERROR"

def test_input_validation():
    """Requirement: Validate payload types (Pydantic)"""
    headers = {
        "X-Parse-REST-API-Key": API_KEY,
        "X-JWT-KWY": VALID_JWT
    }
    # timeToLifeSec should be int, passing string
    payload = {
        "message": "test",
        "to": "me",
        "from": "you",
        "timeToLifeSec": "not-an-int" 
    }
    response = client.post("/DevOps", json=payload, headers=headers)
    assert response.status_code == 422 # FastAPI default validation error
