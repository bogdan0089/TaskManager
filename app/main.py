from fastapi import FastAPI
from database.database import async_engine
from app.router_task import router_task
from app.router_user import router_user
from app.router_auth import router_auth
from sqlalchemy.exc import OperationalError
import asyncio
app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Task Manager API"
    }

app.include_router(router_task)
app.include_router(router_user)
app.include_router(router_auth)

async def wait_for_db(engine, retries=10, delay=2):
    for i in range(retries):
        try:
            async with engine.begin() as conn:
                return
        except OperationalError:
            print(f"DB not ready, retry {i+1}/{retries}")
            await asyncio.sleep(delay)
    raise RuntimeError("Cannot connect to the database")


@app.on_event("startup")
async def startup():
    await wait_for_db(async_engine)