import uuid
from fastapi.testclient import TestClient


def test_create_user_success(client: TestClient):
    response = client.post("/user/create_user", json={
        "name": "Bohdan",
        "email": f"user_{uuid.uuid4().hex[:8]}@gmail.com",
        "role": "worker",
        "password": "1234"
    })
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Bohdan"
    assert data["role"] == "worker"
    assert "id" in data


def test_create_user_duplicate_email(client: TestClient):
    payload = {
        "name": "Bohdan",
        "email": f"user_{uuid.uuid4().hex[:8]}@gmail.com",
        "role": "worker",
        "password": "1234"
    }
    client.post("/user/create_user", json=payload)
    response = client.post("/user/create_user", json=payload)
    assert response.status_code == 409


def test_all_users_as_admin(client: TestClient, admin_headers: dict):
    response = client.get("/user/all_users", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_all_users_as_worker(client: TestClient, worker_headers: dict):
    response = client.get("/user/all_users", headers=worker_headers)
    assert response.status_code == 403


def test_all_users_without_token(client: TestClient):
    response = client.get("/user/all_users")
    assert response.status_code == 401


def test_get_user_as_owner(client: TestClient, worker_headers: dict, new_user: dict):
    login = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    user_id = login.json()["user_id"]
    response = client.get(f"/user/{user_id}", headers=worker_headers)
    assert response.status_code == 200
    assert response.json()["email"] == new_user["email"]


def test_get_user_not_found(client: TestClient, admin_headers: dict):
    response = client.get("/user/99999999", headers=admin_headers)
    assert response.status_code == 404


def test_update_user_as_owner(client: TestClient, worker_headers: dict, new_user: dict):
    login = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    user_id = login.json()["user_id"]
    response = client.patch(
        f"/user/{user_id}/patch",
        json={"name": "New Name", "email": new_user["email"], "role": "worker"},
        headers=worker_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_update_user_as_another_worker(client: TestClient, worker_headers: dict):
    other = client.post("/auth/register", json={
        "name": "Other",
        "email": f"other_{uuid.uuid4().hex[:8]}@gmail.com",
        "role": "worker",
        "password": "1234"
    })
    other_id = other.json()["id"]
    response = client.patch(
        f"/user/{other_id}/patch",
        json={"name": "Hacked", "email": "x@x.com", "role": "worker"},
        headers=worker_headers
    )
    assert response.status_code == 403


def test_delete_user_as_admin(client: TestClient, admin_headers: dict):
    created = client.post("/user/create_user", json={
        "name": "ToDelete",
        "email": f"delete_{uuid.uuid4().hex[:8]}@gmail.com",
        "role": "worker",
        "password": "1234"
    })
    user_id = created.json()["id"]
    response = client.delete(f"/user/{user_id}/delete", headers=admin_headers)
    assert response.status_code == 200


def test_delete_user_as_worker(client: TestClient, worker_headers: dict):
    created = client.post("/user/create_user", json={
        "name": "ToDelete",
        "email": f"delete_{uuid.uuid4().hex[:8]}@gmail.com",
        "role": "worker",
        "password": "1234"
    })
    user_id = created.json()["id"]
    response = client.delete(f"/user/{user_id}/delete", headers=worker_headers)
    assert response.status_code == 403


def test_user_tasks_as_owner(client: TestClient, worker_headers: dict, new_user: dict, new_task: dict):
    login = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    user_id = login.json()["user_id"]
    response = client.get(f"/user/{user_id}/tasks_user", headers=worker_headers)
    tasks = response.json()
    assert response.status_code == 200
    assert isinstance(tasks, list)
    assert any(t["id"] == new_task["id"] for t in tasks)


def test_user_tasks_as_admin(client: TestClient, admin_headers: dict, new_user: dict, new_task: dict):
    login = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    user_id = login.json()["user_id"]
    response = client.get(f"/user/{user_id}/tasks_user", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_user_tasks_as_another_worker(client: TestClient, worker_headers: dict):
    other = client.post("/user/create_user", json={
        "name": "OtherWorker",
        "email": f"other_{uuid.uuid4().hex[:8]}@gmail.com",
        "role": "worker",
        "password": "1234"
    })
    other_id = other.json()["id"]
    response = client.get(f"/user/{other_id}/tasks_user", headers=worker_headers)
    assert response.status_code == 403


def test_user_tasks_not_found(client: TestClient, admin_headers: dict):
    response = client.get("/user/99999999/tasks_user", headers=admin_headers)
    assert response.status_code == 404


def test_user_tasks_without_token(client: TestClient, new_user: dict):
    login = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    user_id = login.json()["user_id"]
    response = client.get(f"/user/{user_id}/tasks_user")
    assert response.status_code == 401
