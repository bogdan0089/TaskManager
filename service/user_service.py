from fastapi import HTTPException, status
from models.models import User
from schemas.schemas_user import CreateUser, UserUpdate
from database.unit_of_work import UnitOfWork
from core.enum import UserRole


class ServiceUser:


    @staticmethod
    async def create_user(data: CreateUser) -> User:
        async with UnitOfWork() as uow:
            user = await uow.user.create_user(data)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            return user
        

    @staticmethod
    async def get_user(user_id: int) -> User:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            return user
        

    @staticmethod
    async def all_users() -> list[User]:
        async with UnitOfWork() as uow:
            users = await uow.user.all_users()
            if not users:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found.")
            return users
        
    
    @staticmethod
    async def check_role_user(user_id: int, data: UserRole) -> User:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            if user.role != data:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="403")
            return user
            
                
    @staticmethod
    async def update_user(user_id: int, user: User, data: UserUpdate) -> User:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            user_update = await uow.user.update_user(user, data)
            if not user_update:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="403")
            return user_update
        

    @staticmethod
    async def delete_user(user_id: int) -> dict:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            user = await uow.user.delete_user(user)
            return {
                "message": "User delete."
            }

    @staticmethod
    async def user_tasks(user_id: int) -> int:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            tasks_user = await uow.user.get_task_user(user_id)
            return tasks_user
