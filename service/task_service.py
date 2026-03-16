from fastapi import HTTPException, status
from database.unit_of_work import UnitOfWork
from schemas.schemas_task import CreateTask, TaskUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Task
from core.enum import TaskStatus



class ServiceTask:
    def __init__(self, session: AsyncSession):
        self.session = session



    @staticmethod
    async def create_task(data: CreateTask, user_id: int) -> Task:
        async with UnitOfWork() as uow:
            task = await uow.task.create_task(data, user_id)
            if not task:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="400")
            return task


    @staticmethod
    async def get_task(task_id: int) -> Task:
        async with UnitOfWork() as uow:
            task = await uow.task.get_task(task_id)
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
            return task


    @staticmethod
    async def create_task_for_user(user_id: int, data: CreateTask) -> dict:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            task = await uow.task.create_task(data, user_id)
            if not task:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="400")
            return task


    @staticmethod
    async def update_task(task_id: int, task: Task, data: TaskUpdate) -> Task:
        async with UnitOfWork() as uow:
            task = await uow.task.get_task(task_id)
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
            update_task = await uow.task.update_task(data)
            if not update_task:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="403")
            return update_task
            

    @staticmethod
    async def delete_task(task_id: int):
        async with UnitOfWork() as uow:
            task = await uow.task.get_task(task_id)
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
            task = await uow.task.task_delete(task_id)
            return task


    @staticmethod
    async def all_tasks() -> list[Task]:
        async with UnitOfWork() as uow:
            tasks = await uow.task.all_tasks()
            if not tasks:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found.")
            return tasks
        

    @staticmethod
    async def change_status(task_id: int, data: TaskStatus):
        async with UnitOfWork() as uow:
            task = await uow.task.get_task(task_id)
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
            change_status = await uow.task.change_status(data)
            if not change_status:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="403")
            return change_status


    @staticmethod
    async def get_task_status(status: TaskStatus) -> list[Task]:
        async with UnitOfWork() as uow:
            return await uow.task.get_task_status(status)
        
    @staticmethod
    async def tasks_stats() -> dict[str, int]:
        async with UnitOfWork() as uow:
            return await uow.task.get_task_stats()