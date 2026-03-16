from fastapi import APIRouter
from schemas.schemas_task import ResponseTask, CreateTask
from service.task_service import ServiceTask
from core.enum import TaskStatus


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


@router_task.get("/all_tasks", response_model=list[ResponseTask])
async def all_tasks():
    return await ServiceTask.all_tasks()


@router_task.patch("/task/{task_id}status", response_model=ResponseTask)
async def change_status(task_id: int, data: TaskStatus):
    return await ServiceTask.change_status(task_id, data)


@router_task.delete("/{task_id}")
async def delete_task(task_id: int):
    return await ServiceTask.delete_task(task_id)


@router_task.get("/task_status", response_model=list[ResponseTask])
async def get_task_status(statu: TaskStatus):
    return await ServiceTask.get_task_status(statu)



@router_task.get("/task_stats", response_model=list[ResponseTask])
async def get_stats():
    return ServiceTask.tasks_stats()