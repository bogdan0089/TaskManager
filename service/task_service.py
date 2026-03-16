from fastapi import HTTPException, status
from database.unit_of_work import UnitOfWork
from schemas.schemas_task import CreateTask
from sqlalchemy.ext.asyncio import AsyncSession





class ServiceTask:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_task(data: CreateTask, user_id: int):
        async with UnitOfWork() as uow:
            task = await uow.task.create_task(data, user_id)
            if not task:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="400")
            return task
        


    async def get_task(task_id: int):
        async with UnitOfWork() as uow:
            task = await uow.task.get_task(task_id)
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
            return task


    # async def task_update(task_id: int, Status: str):
    #     async with UnitOfWork() as uow:
    #         task = await uow.task.get_task(task_id)
    #         if not task:
    #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
            
    #         return await uow.task.



    async def create_task_for_user(user_id: int, data: CreateTask) -> dict:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            task = await uow.task.create_task(data, user_id)
            if not task:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="400")
            return task
