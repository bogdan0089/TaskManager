from models.models import User
from schemas.schemas_user import CreateUser, UserUpdate
from database.unit_of_work import UnitOfWork
from utils.hash import hash_password
from core.enum import UserRole
from core.exceptions import (
    UserAlreadyError,
    UserNotFoundError,
    UsersNotFoundError,
    UserUpdateError,
    UserDeleteError,
    InvalidRoleUser,
    InsufficientPermissionsError,
    TasksNotFoundError
)


class ServiceUser:

    @staticmethod
    async def create_user(data: CreateUser) -> User:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user_by_email(data.email)
            if user:
                raise UserAlreadyError(data.email)
            hashed = hash_password(data.password)
            user = await uow.user.create_user(
                name=data.name,
                email=data.email,
                roel=data.role,
                hashed_password=hashed
            )
            return user
        
    @staticmethod
    async def get_user(user_id: int, current_user: User) -> User:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if user is None:
                raise UserNotFoundError(user_id=user_id)
            if current_user.id != user_id and current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Admin or owner",
                    user_role=current_user.role.value
                )
            return user
            
    @staticmethod
    async def all_users(current_user: User) -> list[User]:
        async with UnitOfWork() as uow:
            users = await uow.user.all_users()
            if users is None:
                raise UsersNotFoundError()
            if current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="admin",
                    user_role=current_user.role.value
                )
            return users
        
    @staticmethod
    async def check_role_user(user_id: int, required_role: UserRole, current_user: User) -> User:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if user is None:
                raise UserNotFoundError(user_id=user_id)
            if current_user.id != user_id and current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Admin or owner",
                    user_role=current_user.role.value
                )
            if user.role != required_role:
                raise InvalidRoleUser(expected_role=required_role.value, actual_role=user.role.value if user.role else "None")
            return user
        
    @staticmethod
    async def update_user(user_id: int, data: UserUpdate, current_user: User) -> User:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if user is None:
                raise UserNotFoundError(user_id=user_id)
            if current_user.id != user_id:
                if current_user.role != UserRole.admin:
                    raise InsufficientPermissionsError(
                        required_role="Admin or some user.",
                        user_role=current_user.role.value if current_user.role else "None"
                    )
            if data.email and data.email != user.email:
                existing_user = await uow.user.get_user_by_email(data.email)
                if existing_user:
                    raise UserAlreadyError(data.email)
            update_user = await uow.user.update_user(user, data)
            if update_user is None:
                raise UserUpdateError(reason="Error update")
            return update_user
        
    @staticmethod
    async def delete_user(user_id: int, current_user: User) -> dict:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if user is None:
                raise UserNotFoundError(user_id)
            if current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Only admin",
                    user_role=current_user.role.value
                )
            user_delete = await uow.user.delete_user(user_id)
            if user_delete is None:
                raise UserDeleteError(reason="Failed to delete.")
            return user_delete
        
    @staticmethod
    async def user_tasks(user_id: int, current_user: User) -> int:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if user is None:
                raise UserNotFoundError(user_id)
            if current_user.id != user_id and current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Admin or owner",
                    user_role=current_user.role.value
                )
            tasks_user = await uow.user.get_task_user(user_id)
            if tasks_user is None:
                raise TasksNotFoundError()
            return tasks_user
        
    
