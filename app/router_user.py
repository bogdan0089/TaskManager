from fastapi import APIRouter
from schemas.schemas_user import CreateUser, ResponseUser
from schemas.schemas_task import ResponseTask
from service.user_service import ServiceUser
from core.enum import UserRole

router_user = APIRouter(prefix="/user")





@router_user.post("/create_user", response_model=ResponseUser)
async def create_user(data: CreateUser):
    return await ServiceUser.create_user(data)


@router_user.get("/all_users", response_model=list[ResponseUser])
async def all_users():
    return await ServiceUser.all_users()


@router_user.get("/{user_id}", response_model=ResponseUser)
async def get_user(user_id: int):
    return await ServiceUser.get_user(user_id)


@router_user.get("/{user_id}/status", response_model=ResponseUser)
async def check_status_user(user_id: int, data: UserRole):
    user = await ServiceUser.check_role_user(user_id, data.admin)
    return {
        "message": f"Hello Admin:{user.name}!"
    }


@router_user.patch("/{user_id}/patch", response_model=ResponseUser)
async def update_user(user_id: int):
    return await ServiceUser.update_user(user_id)


@router_user.delete("/{user_id}/delete")
async def delete_user(user_id: int):
    return await ServiceUser.delete_user(user_id)


@router_user.get("/{user_id}/tasks_user", response_model=list[ResponseTask])
async def user_tasks(user_id: int):
    return await ServiceUser.user_tasks(user_id)


