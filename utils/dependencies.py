from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from database.unit_of_work import UnitOfWork
from service.auth_service import AuthService
from core.exceptions import UserNotFoundError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = AuthService.decode_token(token)
    async with UnitOfWork() as uow:
        user = await uow.user.get_user(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user
