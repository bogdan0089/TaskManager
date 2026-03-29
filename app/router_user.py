from fastapi import APIRouter, Depends
from schemas.schemas_user import CreateUser, ResponseUser, UserUpdate
from schemas.schemas_task import ResponseTask
from service.user_service import ServiceUser
from core.enum import UserRole
from utils.dependencies import get_current_user


router_user = APIRouter(prefix="/user")


@router_user.post("/create_user", response_model=ResponseUser)
async def create_user(data: CreateUser):
    user = await ServiceUser.create_user(data)
    return user

@router_user.get("/all_users", response_model=list[ResponseUser])
async def all_users(current_user=Depends(get_current_user)):
    return await ServiceUser.all_users(current_user)

@router_user.get("/{user_id}", response_model=ResponseUser)
async def get_user(user_id: int, current_user=Depends(get_current_user)):
    return await ServiceUser.get_user(user_id, current_user)

@router_user.get("/{user_id}/status", response_model=ResponseUser)
async def check_status_user(user_id: int, data: UserRole, current_user=Depends(get_current_user)):
    user = await ServiceUser.check_role_user(user_id, data, current_user)
    return user

@router_user.patch("/{user_id}/patch", response_model=ResponseUser)
async def update_user(user_id: int, data: UserUpdate, current_user=Depends(get_current_user)):
    return await ServiceUser.update_user(user_id, data, current_user)

@router_user.delete("/{user_id}/delete")
async def delete_user(user_id: int, current_user=Depends(get_current_user)):
    return await ServiceUser.delete_user(user_id, current_user)

@router_user.get("/{user_id}/tasks_user", response_model=list[ResponseTask])
async def user_tasks(user_id: int, current_user=Depends(get_current_user)):
    return await ServiceUser.user_tasks(user_id, current_user)


