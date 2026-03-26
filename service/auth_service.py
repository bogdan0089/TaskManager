from datetime import timedelta, datetime, timezone
from core.cfg import settings
from database.unit_of_work import UnitOfWork
from core.exceptions import UserNotFoundError, UserAlreadyError, UserUpdateError
from utils.hash import hash_password, verify_password
from schemas.schemas_user import CreateUser
from schemas.schemas_auth import TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
import jwt

class AuthService:

    def create_access_token(user_id: int):
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCES_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

    def decode_token(token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise UserNotFoundError(user_id)
            return int(user_id)
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired.")
        except jwt.InvalidTokenError:
            raise Exception("Invalid Token.")

    def create_refresh_token(user_id: int):
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(days=settings.DAYS)
        }
        return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

    @staticmethod
    async def register_user(data: CreateUser):
        async with UnitOfWork() as uow:
            existing = await uow.user.get_user_by_email(data.email)
            if existing:
                raise UserAlreadyError(data.email)
            
            hashed = hash_password(data.password)

            user = await uow.user.create_user(
                name=data.name,
                email=data.email,
                role=data.role,
                hashed_password=hashed
            )
            if user is None:
                raise UserUpdateError("Failed! CreateUser.")
            return user
    
    @staticmethod
    async def user_login(data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
        async with UnitOfWork() as uow:
            user = await uow.user.get_user_by_email(data.username)
            if user is None:
                raise UserNotFoundError(email=data.username)
            
            if not verify_password(data.password, user.hashed_password):
                raise UserUpdateError("Error")
            
            token = AuthService.create_access_token(user.id)
            refresh_token = AuthService.create_refresh_token(user.id)
            return TokenResponse(
                access_token=token,
                refresh_token=refresh_token,
                token_type="bearer",
                user_id=user.id,
                email=user.email,
                name=user.name
            )

    @staticmethod
    async def refresh_token(token: str):
        user_id = AuthService.decode_token(token)
        new_access = AuthService.create_access_token(user_id)
        return {"access_token": new_access, "token_type": "bearer"}
    


                






















