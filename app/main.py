from fastapi import FastAPI
from database.database import Base, async_engine
from app.router_task import router_task
from app.router_user import router_user


app = FastAPI()


@app.get("/")
async def root():
    return await {
        "message": "Task Manager API"
    }

app.include_router(router_task)
app.include_router(router_user)


@app.on_event("startup")
async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)