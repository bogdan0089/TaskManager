from fastapi import HTTPException, status
from database.unit_of_work import UnitOfWork
from schemas.schemas_task import CreateTask, TaskUpdate
from models.models import Task, User
from core.enum import TaskStatus, UserRole
from core.exceptions import (
    TasksNotFoundError,
    TaskUpdateError,
    TaskDeleteError,
    TaskNotFound,
    TaskAlreadyError,
    UserNotFoundError,
    InsufficientPermissionsError,
)


class ServiceTask:

    @staticmethod
    async def create_task(data: CreateTask, user_id: int) -> Task:
        async with UnitOfWork() as uow:
            existing_task = await uow.task.get_by_title_and_user(data.title, user_id)
            if existing_task:
                raise TaskAlreadyError(task_id=existing_task.id)
            create_task = await uow.task.create_task(data, user_id)
            return create_task

    @staticmethod
    async def get_task(task_id: int, current_user: User) -> Task:
        async with UnitOfWork() as uow:
            task = await uow.task.get_task(task_id)
            if task is None:
                raise TaskNotFound(task_id)
            if task.user_id != current_user.id and current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Admin or owner",
                    user_role=current_user.role.value
                )
            return task

    @staticmethod
    async def create_task_for_user(user_id: int, data: CreateTask, current_user: User) -> dict:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if user is None:
                raise UserNotFoundError(user_id)
            if current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Only Admin",
                    user_role=current_user.role.value
                )
            task = await uow.task.create_task(data, user_id)
            if task is None:
                raise TaskUpdateError(reason="Failed to create task.")
            return {
                "user": {
                    "id": user_id,
                    "email": user.email, 
                    "name": user.name
                },
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status
                }
            }

    @staticmethod
    async def update_task(task_id: int, task: Task, data: TaskUpdate, current_user: User) -> Task:
        async with UnitOfWork() as uow:
            task = await uow.task.get_task(task_id)
            if task is None:
                raise TaskNotFound(f"Not found task with id: {task_id}")
            if task.user_id != current_user.id and current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Admin or owner",
                    user_role=current_user.role.value
                )
            update_task = await uow.task.update_task(task, data)
            if update_task is None:
                raise TaskUpdateError(reason="Failed to update.")
            return update_task
            
    @staticmethod
    async def delete_task(task_id: int, current_user: User):
        async with UnitOfWork() as uow:
            task = await uow.task.get_task(task_id)
            if task is None:
                raise TaskNotFound(task_id)
            if current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Only admin",
                    user_role=current_user.role.value
                )
            task = await uow.task.task_delete(task_id)
            if task is None:
                raise TaskDeleteError(reason="Failed to delete.")
            return task

    @staticmethod
    async def all_tasks(curent_user: User, limit: int=10, offset: int=10) -> list[Task]:
        async with UnitOfWork() as uow:
            tasks = await uow.task.all_tasks(limit=limit, offset=offset)
            if tasks is None:
                raise TasksNotFoundError()
            if curent_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Only admin",
                    user_role=curent_user.role.value
                )
            return tasks
        
    @staticmethod
    async def change_status(task_id: int, data: TaskStatus, current_user: User):
        async with UnitOfWork() as uow:
            task = await uow.task.get_task(task_id)
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
            change_status = await uow.task.change_status(data)
            if not change_status:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="403")
            if task.user_id != current_user.id and current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Admin or owner",
                    user_role=current_user.role.value
                )
            return change_status

    @staticmethod
    async def get_task_status(status: TaskStatus, current_user: User) -> list[Task]:
        async with UnitOfWork() as uow:
            status = await uow.task.get_task_status(status)
            if current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Only admin",
                    user_role=current_user.role.value
                )
            return status
        
    @staticmethod
    async def tasks_stats(current_user: User) -> dict[str, int]:
        async with UnitOfWork() as uow:
            task = await uow.task.get_task_stats()
            if current_user.role != UserRole.admin:
                raise InsufficientPermissionsError(
                    required_role="Only admin",
                    user_role=current_user.role.value
                )
            return task