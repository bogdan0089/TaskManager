from fastapi import APIRouter
from schemas.schemas_task import ResponseTask, CreateTask
from service.task_service import ServiceTask



router_task = APIRouter(prefix="/task")




@router_task.post("/create_task", response_model=ResponseTask)
async def create_task(data: CreateTask):
    return await ServiceTask.create_task(data)


@router_task.get("/{task_id}", response_model=ResponseTask)
async def get_task(task_id: int):
    return await ServiceTask.get_task(task_id)


@router_task.post("/user/{user_id}", response_model=ResponseTask)
async def create_task_for_user(user_id: int, data: CreateTask):
    return await ServiceTask.create_task_for_user(user_id, data)

