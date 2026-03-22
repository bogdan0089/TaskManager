from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas_task import CreateTask, TaskUpdate
from models.models import Task
from sqlalchemy import select, func
from core.enum import TaskStatus


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        

    async def create_task(self, data: CreateTask, user_id: int) -> Task:
        create_task = Task(
            title=data.title,
            status=data.status,
            user_id=user_id
        )
        self.session.add(create_task)
        await self.session.flush()
        await self.session.refresh(create_task)
        return create_task

    async def get_task(self, task_id: int) -> Task:
        task = await self.session.get(Task, task_id)
        return task

    async def update_task(self, task: Task, data: TaskUpdate) -> Task:
        task.title = data.title
        task.status = data.status
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
        return task

    async def task_delete(self, task: Task):
        task = await self.session.delete(task)
        return task

    async def all_tasks(self, limit: int, offset: int):
        task = await self.session.execute(
            select(Task).limit(limit).offset(offset)
        )
        return task.scalars().all()
    
    async def change_status(self, task: Task, data: TaskStatus):
        task.status = data
        await self.session.flush()
        await self.session.refresh(task)
        return task

    async def get_task_status(self, statu: TaskStatus) -> list[Task]:
        result = await self.session.execute(
            select(Task).where(Task.status == statu)
        )
        return result.scalars().all()
    
    async def get_task_stats(self) -> dict[str, int]:
        result = await self.session.execute(
            select(Task.status, func.count(Task.id).label("count"))
            .group_by(Task.status)
        )
        rows = result.all()
        return {status: count for status, count in rows}

    async def get_by_title_and_user(self, title: str, user_id: int) -> Task | None:
        result = await self.session.execute(
            select(Task)
            .where(Task.title == title, Task.user_id == user_id)
        )
        return result.scalars().first()
    
    