from fastapi.testclient import TestClient


def test_create_task_success(client: TestClient, worker_headers: dict):
    response = client.post("/task/create_task", json={
        "title": "My first task",
        "status": "in_progress"
    }, headers=worker_headers)
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "My first task"
    assert data["status"] == "in_progress"
    assert "id" in data


def test_create_task_without_token(client: TestClient):
    response = client.post("/task/create_task", json={
        "title": "My task",
        "status": "in_progress"
    })
    assert response.status_code == 401


def test_create_task_invalid_status(client: TestClient, worker_headers: dict):
    response = client.post("/task/create_task", json={
        "title": "My task",
        "status": "flying"  # такого статусу не існує
    }, headers=worker_headers)
    assert response.status_code == 422


def test_all_tasks_success(client: TestClient, admin_headers: dict, new_task: dict):
    response = client.get("/task/all_tasks", headers=admin_headers)
    tasks = response.json()
    assert response.status_code == 200
    assert isinstance(tasks, list)
    assert any(t["id"] == new_task["id"] for t in tasks)


def test_all_tasks_as_worker(client: TestClient, worker_headers: dict):
    response = client.get("/task/all_tasks", headers=worker_headers)
    assert response.status_code == 403


def test_all_tasks_without_token(client: TestClient):
    response = client.get("/task/all_tasks")
    assert response.status_code == 401


def test_get_task_success(client: TestClient, worker_headers: dict, new_task: dict):
    task_id = new_task["id"]
    response = client.get(f"/task/{task_id}", headers=worker_headers)
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == new_task["title"]


def test_get_task_not_found(client: TestClient, worker_headers: dict):
    response = client.get("/task/99999999", headers=worker_headers)
    assert response.status_code == 404


def test_update_task_success(client: TestClient, worker_headers: dict, new_task: dict):
    task_id = new_task["id"]
    response = client.patch(f"/task/{task_id}", json={
        "title": "Updated title",
        "status": "done"
    }, headers=worker_headers)
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Updated title"
    assert data["status"] == "done"


def test_update_task_without_token(client: TestClient, new_task: dict):
    task_id = new_task["id"]
    response = client.patch(f"/task/{task_id}", json={
        "title": "Hacked",
        "status": "done"
    })
    assert response.status_code == 401


def test_delete_task_success(client: TestClient, admin_headers: dict, new_task: dict):
    task_id = new_task["id"]
    response = client.delete(f"/task/{task_id}", headers=admin_headers)
    assert response.status_code == 200


def test_delete_task_as_worker(client: TestClient, worker_headers: dict, new_task: dict):
    task_id = new_task["id"]
    response = client.delete(f"/task/{task_id}", headers=worker_headers)
    assert response.status_code == 403


def test_delete_task_not_found(client: TestClient, worker_headers: dict):
    response = client.delete("/task/99999999", headers=worker_headers)
    assert response.status_code == 403


def test_delete_task_without_token(client: TestClient, new_task: dict):
    task_id = new_task["id"]
    response = client.delete(f"/task/{task_id}")
    assert response.status_code == 401


def test_task_status_as_admin(client: TestClient, admin_headers: dict, new_task: dict):
    response = client.get("/task/task_status?statu=in_progress", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_task_status_as_worker(client: TestClient, worker_headers: dict):
    response = client.get("/task/task_status?statu=in_progress", headers=worker_headers)
    assert response.status_code == 403


def test_task_status_without_token(client: TestClient):
    response = client.get("/task/task_status?statu=in_progress")
    assert response.status_code == 401


def test_task_status_invalid_value(client: TestClient, admin_headers: dict):
    response = client.get("/task/task_status?statu=flying", headers=admin_headers)
    assert response.status_code == 422


def test_task_stats_as_admin(client: TestClient, admin_headers: dict, new_task: dict):
    response = client.get("/task/task_stats", headers=admin_headers)
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)


def test_task_stats_as_worker(client: TestClient, worker_headers: dict):
    response = client.get("/task/task_stats", headers=worker_headers)
    assert response.status_code == 403


def test_task_stats_without_token(client: TestClient):
    response = client.get("/task/task_stats")
    assert response.status_code == 401


def test_create_task_for_user_as_admin(client: TestClient, admin_headers: dict, new_user: dict):
    login = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    user_id = login.json()["user_id"]
    response = client.post(f"/task/user/{user_id}", json={
        "title": "Admin created this task",
        "status": "in_progress"
    }, headers=admin_headers)
    data = response.json()
    assert response.status_code == 200
    assert data["task"]["title"] == "Admin created this task"
    assert data["user"]["id"] == user_id


def test_create_task_for_user_as_worker(client: TestClient, worker_headers: dict, new_user: dict):
    login = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    user_id = login.json()["user_id"]
    response = client.post(f"/task/user/{user_id}", json={
        "title": "Sneaky task",
        "status": "in_progress"
    }, headers=worker_headers)
    assert response.status_code == 403


def test_create_task_for_nonexistent_user(client: TestClient, admin_headers: dict):
    response = client.post("/task/user/99999999", json={
        "title": "Task for nobody",
        "status": "in_progress"
    }, headers=admin_headers)
    assert response.status_code == 404


def test_change_status_success(client: TestClient, worker_headers: dict, new_task: dict):
    task_id = new_task["id"]
    response = client.patch(
        f"/task/{task_id}/status",
        json="done",
        headers=worker_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_change_status_not_found(client: TestClient, worker_headers: dict):
    response = client.patch(
        "/task/99999999/status",
        json="done",
        headers=worker_headers
    )
    assert response.status_code == 404


def test_change_status_without_token(client: TestClient, new_task: dict):
    task_id = new_task["id"]
    response = client.patch(f"/task/{task_id}/status", json="done")
    assert response.status_code == 401


def test_my_stats_success(client: TestClient, worker_headers: dict, new_task: dict):
    response = client.get("/task/my/stats", headers=worker_headers)
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)


def test_my_stats_without_token(client: TestClient):
    response = client.get("/task/my/stats")
    assert response.status_code == 401


def test_tasks_for_admin_success(client: TestClient, admin_headers: dict, new_task: dict, new_user: dict):
    login = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    user_id = login.json()["user_id"]
    response = client.get(f"/task/{user_id}/tasks_for_admin", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(t["id"] == new_task["id"] for t in response.json())


def test_tasks_for_admin_as_worker(client: TestClient, worker_headers: dict, new_user: dict):
    login = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    user_id = login.json()["user_id"]
    response = client.get(f"/task/{user_id}/tasks_for_admin", headers=worker_headers)
    assert response.status_code == 403


def test_tasks_for_admin_without_token(client: TestClient, new_user: dict):
    login = client.post("/auth/user_login", data={
        "username": new_user["email"],
        "password": new_user["password"]
    })
    user_id = login.json()["user_id"]
    response = client.get(f"/task/{user_id}/tasks_for_admin")
    assert response.status_code == 401


def test_my_tasks_success(client: TestClient, worker_headers: dict, new_task: dict):
    response = client.get("/task/my_tasks", headers=worker_headers)
    tasks = response.json()
    assert response.status_code == 200
    assert isinstance(tasks, list)
    assert any(t["id"] == new_task["id"] for t in tasks)


def test_my_tasks_without_token(client: TestClient):
    response = client.get("/task/my_tasks")
    assert response.status_code == 401


def test_search_task_success(client: TestClient, worker_headers: dict, new_task: dict):
    title = new_task["title"]
    response = client.get(f"/task/search?title={title}", headers=worker_headers)
    tasks = response.json()
    assert response.status_code == 200
    assert isinstance(tasks, list)
    assert any(t["id"] == new_task["id"] for t in tasks)


def test_search_task_as_admin(client: TestClient, admin_headers: dict, new_task: dict):
    title = new_task["title"]
    response = client.get(f"/task/search?title={title}", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_task_not_found(client: TestClient, worker_headers: dict):
    response = client.get("/task/search?title=zzz_no_such_task_zzz", headers=worker_headers)
    assert response.status_code == 404


def test_search_task_without_token(client: TestClient):
    response = client.get("/task/search?title=test")
    assert response.status_code == 401
