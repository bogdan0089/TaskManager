# Task Manager API

**Task Manager API** is a FastAPI project for managing users and tasks with async PostgreSQL, JWT authentication, and basic roles (`admin` / `worker`).

---

## Technologies

- Python 3.11
- FastAPI
- SQLAlchemy ORM (async)
- PostgreSQL
- Docker / Docker Compose
- JWT
- Pydantic schemas
- Alembic
- Clean code
- Unit of Work pattern
- Pytest

---

## Running the Project

Clone the repository:

```bash
git clone https://github.com/bogdan0089/TaskManager
cd ManagerTask
```

Create `.env` from example:

```bash
cp .env.example .env
```

Fill in your values in `.env`, then start:

```bash
docker-compose up --build
```
