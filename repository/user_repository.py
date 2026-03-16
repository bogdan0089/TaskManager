from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User, Task
from sqlalchemy import select, func
from schemas.schemas_user import CreateUser



class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_user(self, data: CreateUser) -> User:
        user = User(
            name=data.name,
            email=data.email,
            role=data.role            
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user


    async def get_user(self, user_id: int) -> User:
        user = await self.session.get(User, user_id)
        return user
        

    async def delete_user(self, user: User) -> User:
        user = await self.session.delete(user)
        return user


    async def update_user(self, user: User, data: CreateUser) -> User:
        if user.name:
            user.name = data.name
        if user.email:
            user.email = data.email
        if user.role:
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