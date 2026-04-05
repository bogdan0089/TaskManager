# Task Manager API

Production-ready REST API for managing users and tasks with role-based access control, built with async FastAPI and PostgreSQL.

## Features

- JWT authentication (access + refresh tokens)
- Role-based access control (admin / worker)
- Task assignment, filtering by status, search by title
- Task and user statistics
- Password change
- Database migrations with Alembic
- Fully containerized with Docker Compose
- Unit & integration tests with Pytest

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (async) |
| Database | PostgreSQL + SQLAlchemy 2.0 ORM |
| Migrations | Alembic |
| Auth | JWT (PyJWT) + bcrypt |
| Validation | Pydantic v2 |
| Architecture | Clean Architecture, Repository + Service pattern, Unit of Work |
| Infrastructure | Docker, Docker Compose |
| Testing | Pytest |

## Project Structure
```
├── app/          # FastAPI routers
├── service/      # Business logic
├── repository/   # Database queries
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic schemas
├── core/         # Config, enums, exceptions
├── database/     # Session, Unit of Work
├── utils/        # JWT, dependencies
└── alembic/      # Migrations
```

## API Endpoints

### Auth
| Method | URL | Auth | Description |
|---|---|---|---|
| POST | /auth/register | 🔓 | Register new user |
| POST | /auth/user_login | 🔓 | Login, get tokens |
| GET | /auth/me | 🔒 | Get current user |
| POST | /auth/refresh | 🔓 | Refresh access token |
| PATCH | /auth/change_password | 🔒 | Change password |

### Users
| Method | URL | Auth | Description |
|---|---|---|---|
| POST | /user/create_user | 🔓 | Create user |
| GET | /user/all_users | 🔒 | List all users |
| GET | /user/{user_id} | 🔒 | Get user by ID |
| GET | /user/{user_id}/status | 🔒 | Check user role |
| PATCH | /user/{user_id}/patch | 🔒 | Update user |
| DELETE | /user/{user_id}/delete | 🔒 | Delete user |
| GET | /user/{user_id}/tasks_user | 🔒 | Get user's tasks |

### Tasks
| Method | URL | Auth | Description |
|---|---|---|---|
| POST | /task/create_task | 🔒 | Create task |
| GET | /task/all_tasks | 🔒 | List all tasks |
| GET | /task/my_tasks | 🔒 | My tasks |
| GET | /task/search | 🔒 | Search tasks by title |
| GET | /task/task_status | 🔒 | Filter tasks by status |
| GET | /task/task_stats | 🔒 | Task statistics |
| GET | /task/my/stats | 🔒 | My personal stats |
| GET | /task/{task_id} | 🔒 | Get task by ID |
| POST | /task/user/{user_id} | 🔒 Admin | Assign task to user |
| PATCH | /task/{task_id} | 🔒 | Update task |
| PATCH | /task/{task_id}/status | 🔒 | Change task status |
| DELETE | /task/{task_id} | 🔒 | Delete task |
| GET | /task/{user_id}/tasks_for_admin | 🔒 Admin | View user tasks (admin) |

## Getting Started
```bash
git clone https://github.com/bogdan0089/TaskManager
cd TaskManager
cp .env.example .env
docker compose up --build
```

API docs available at: `http://localhost:8000/docs`