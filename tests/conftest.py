import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def new_user(client):
    payload = {
        "name": "Bohdan",
        "email": f"worker_{uuid.uuid4().hex[:8]}@gmail.com",
        "role": "worker",
        "password": "1234"
    }
    client.post("/auth/register", json=payload)
    return payload


@pytest.fixture
def admin_user(client):
    payload = {
        "name": "Admin",
        "email": f"admin_{uuid.uuid4().hex[:8]}@gmail.com",
        "role": "admin",
        "password": "admin1234"
    }
    client.post("/auth/register", json=payload)
    return payload


@pytest.fixture
def worker_headers(client, new_user):
    response = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, admin_user):
    response = client.post("/auth/user_login", data={
        "username": admin_user["email"],
        "password": admin_user["password"]
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def new_task(client, worker_headers):
    payload = {
        "title": "Test Task",
        "status": "in_progress"
    }
    response = client.post("/task/create_task", json=payload, headers=worker_headers)
    return response.json()
