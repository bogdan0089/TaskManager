from database.database import async_engine_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from repository.user_repository import UserRepository
from repository.task_repository import TaskRepository

class UnitOfWork:
    def __init__(self):
        self.session_factory = async_engine_sessionmaker
        self.session: AsyncSession | None = None


    async def __aenter__(self):
        self.session = self.session_factory()
        self.user = UserRepository(self.session)
        self.task = TaskRepository(self.session)
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()


    async def commit(self):
        await self.commit()

    async def rollback(self):
        await self.rollback()
    