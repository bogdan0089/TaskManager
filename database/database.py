from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from core.cfg import DATABASE_URL


async_engine = create_async_engine(DATABASE_URL, echo=True)

async_engine_sessionmaker= sessionmaker(class_=AsyncSession, expire_on_commit=False, bind=async_engine)

class Base(DeclarativeBase):
    pass


async def get_session():
    async with async_engine_sessionmaker() as session:
        yield session