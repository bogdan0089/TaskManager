from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.schemas_auth import TokenResponse
from schemas.schemas_user import CreateUser, UserLogin, ResponseUser
from utils.dependencies import get_current_user
from models.models import User
from service.auth_service import AuthService


router_auth = APIRouter(prefix="/auth")

@router_auth.post("/register", response_model=ResponseUser)
async def register(data: CreateUser):
    return await AuthService.register_user(data)

@router_auth.post("/user_login", response_model=TokenResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends()):
    return await AuthService.user_login(data)

@router_auth.get("/me", response_model=TokenResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
