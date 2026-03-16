from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas_task import CreateTask, TaskUpdate
from models.models import Task




class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        

    async def create_task(self, data: CreateTask, user_id: int):
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

        

    