from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User, Task
from sqlalchemy import select, func
from schemas.schemas_user import UserUpdate
from core.enum import UserRole

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_user(self, name: str, email: str, role: UserRole, hashed_password: str) -> User:
        user = User(
            name=name,
            email=email,
            role=role,
            hashed_password=hashed_password
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def get_user(self, user_id: int) -> User:
        user = await self.session.get(User, user_id)
        return user
    
    async def get_user_by_email(self, email: str) -> User | None:
        stmt = await self.session.execute(
            select(User)
            .where(User.email == email)
        )
        return stmt.scalars().first()

    async def delete_user(self, user: User) -> User:
        user = await self.session.delete(user)
        return user

    async def update_user(self, user: User, data: UserUpdate) -> User:
        if data.name is not None:
            user.name = data.name
        if data.email is not None:
            user.email = data.email
        if data.role is not None:
            user.role = data.role
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def all_users(self) -> list[User]:
        users = await self.session.execute(
            select(User)
        )
        return users.scalars().all()
    
    async def get_task_user(self, user_id: int) -> int:
        stmt = await self.session.execute(
            select(func.count(Task.id)).where(Task.user_id == user_id)
        )
        return stmt.scalar()