import uuid
from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    response = client.post("/auth/register", json={
        "name": "Bohdan",
        "email": f"test_{uuid.uuid4().hex[:8]}@gmail.com",
        "role": "worker",
        "password": "1234"
    })
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Bohdan"
    assert data["role"] == "worker"
    assert "id" in data


def test_register_duplicate_email(client: TestClient):
    payload = {
        "name": "Bohdan",
        "email": f"test_{uuid.uuid4().hex[:8]}@gmail.com",
        "role": "worker",
        "password": "1234"
    }
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409


def test_register_missing_field(client: TestClient):
    response = client.post("/auth/register", json={
        "name": "Bohdan",
        # email 
        "role": "worker",
        "password": "1234"
    })
    assert response.status_code == 422


def test_register_invalid_role(client: TestClient):
    response = client.post("/auth/register", json={
        "name": "Bohdan",
        "email": f"test_{uuid.uuid4().hex[:8]}@gmail.com",
        "role": "superadmin",
        "password": "1234"
    })
    assert response.status_code == 422


def test_login_success(client: TestClient, new_user: dict):
    response = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == new_user["email"]
    assert data["name"] == new_user["name"]


def test_login_wrong_password(client: TestClient, new_user: dict):
    response = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": "WRONG_PASSWORD"
    })
    assert response.status_code == 400


def test_login_not_found(client: TestClient):
    response = client.post("/auth/user_login", data={
        "username": "nobody@gmail.com",
        "password": "1234"
    })
    assert response.status_code == 404


def test_me_success(client: TestClient, worker_headers: dict):
    response = client.get("/auth/me", headers=worker_headers)
    assert response.status_code == 200


def test_me_without_token(client: TestClient):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_refresh_token_success(client: TestClient, new_user: dict):
    login = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    refresh_token = login.json()["refresh_token"]
    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid(client: TestClient):
    response = client.post("/auth/refresh", json={
        "refresh_token": "not.a.valid.token"
    })
    assert response.status_code >= 400


def test_change_password_success(client: TestClient, new_user: dict, worker_headers: dict):
    response = client.patch("/auth/change_password", json={
        "old_password": new_user["password"],
        "new_password": "NewPass999"
    }, headers=worker_headers)
    assert response.status_code == 200


def test_change_password_wrong_old(client: TestClient, worker_headers: dict):
    response = client.patch("/auth/change_password", json={
        "old_password": "WRONG_OLD",
        "new_password": "NewPass999"
    }, headers=worker_headers)
    assert response.status_code == 400


def test_change_password_without_token(client: TestClient):
    response = client.patch("/auth/change_password", json={
        "old_password": "any",
        "new_password": "any"
    })
    assert response.status_code == 401
