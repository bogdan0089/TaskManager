from fastapi import APIRouter, Depends
from schemas.schemas_task import ResponseTask, CreateTask, TaskUpdate
from service.task_service import ServiceTask
from core.enum import TaskStatus
from utils.dependencies import get_current_user


router_task = APIRouter(prefix="/task")

@router_task.get("/search", response_model=list[ResponseTask])
async def search_task(title: str, current_user=Depends(get_current_user)):
    return await ServiceTask.search_task_by_user_id(current_user, title)

@router_task.post("/create_task", response_model=ResponseTask)
async def create_task(data: CreateTask, current_user=Depends(get_current_user)):
    return await ServiceTask.create_task(data, current_user.id)

@router_task.get("/all_tasks", response_model=list[ResponseTask])
async def all_tasks(current_user=Depends(get_current_user)):
    return await ServiceTask.all_tasks(current_user)

@router_task.get("/task_status", response_model=list[ResponseTask])
async def get_task_status(statu: TaskStatus, current_user=Depends(get_current_user)):
    return await ServiceTask.get_task_status(statu, current_user)

@router_task.get("/task_stats", response_model=dict[str, int])
async def get_stats(current_user=Depends(get_current_user)):
    return await ServiceTask.tasks_stats(current_user)

@router_task.get("/my_tasks", response_model=list[ResponseTask])
async def get_my_tasks(current_user=Depends(get_current_user)):
    return await ServiceTask.get_tasks_by_user_id(current_user.id)

@router_task.get("/my/stats")
async def stats_by_user_id(current_user=Depends(get_current_user)):
    return await ServiceTask.get_my_stats(current_user)
    
@router_task.get("/{task_id}", response_model=ResponseTask)
async def get_task(task_id: int, current_user=Depends(get_current_user)):
    return await ServiceTask.get_task(task_id, current_user)

@router_task.post("/user/{user_id}")
async def create_task_for_user(user_id: int, data: CreateTask, current_user=Depends(get_current_user)):
    return await ServiceTask.create_task_for_user(user_id, data, current_user)

@router_task.patch("/{task_id}", response_model=ResponseTask)
async def update_task(task_id: int, data: TaskUpdate, current_user=Depends(get_current_user)):
    return await ServiceTask.update_task(task_id, data, current_user)

@router_task.patch("/{task_id}/status", response_model=ResponseTask)
async def change_status(task_id: int, data: TaskStatus, current_user=Depends(get_current_user)):
    return await ServiceTask.change_status(task_id, data, current_user)

@router_task.delete("/{task_id}")
async def delete_task(task_id: int, current_user=Depends(get_current_user)):
    return await ServiceTask.delete_task(task_id, current_user)

@router_task.get("/{user_id}/tasks_for_admin", response_model=list[ResponseTask])
async def tasks_for_admin(user_id: int, current_user=Depends(get_current_user)):
    return await ServiceTask.get_task_for_admin(user_id, current_user)

