from datetime import timedelta, datetime, timezone
import jwt
from core.cfg import settings
from database.unit_of_work import UnitOfWork
from core.exceptions import UserNotFoundError, UserAlreadyError, UserUpdateError
from utils.hash import hash_password, verify_password
from schemas.schemas_user import CreateUser, UserLogin
from schemas.schemas_auth import TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends


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
            return TokenResponse(
                access_token=token,
                token_type="bearer",
                user_id=user.id,
                email=user.email,
                name=user.name
            )

                




























    # @staticmethod
    # async def register_user(data: CreateUser):
    #     async with UnitOfWork() as uow:
    #         existing_user = await uow.user.get_user_by_email(data.email)
    #         if existing_user:
    #             raise UserAlreadyError(email=data.email)
    #         hashed = hash_password(data.password)
    #         user = await uow.user.create_user(
    #             name=data.name,
    #             email=data.email,
    #             role=data.role,
    #             hashed_password=hashed
    #         )
    #         if user is None:
    #             raise UserUpdateError(reason="Failed to create.")
    #         return user
            

    # @staticmethod
    # async def login(data: UserLogin):
    #     async with UnitOfWork() as uow:

    #         user = await uow.user.get_user_by_email(data.email)
    #         if user is None:
    #             raise UserNotFoundError(email=data.email)
            
    #         if not verify_password(data.password, user.hashed_password):
    #             raise UserNotFoundError(email=data.email)
            
    #         token = AuthService.create_token(user.id)
    #         return {"access token": token}



    # @staticmethod
    # def create_token(user_id: int):
    #     payload = {
    #         "sub": str(user_id),
    #         "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCES_TOKEN_EXPIRE_MINUTES)
    #     }
    #     return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)


    # @staticmethod
    # def decode_token(token: str):
    #     try:
    #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    #     except jwt.ExpiredSignatureError:
    #         raise Exception("Token expired.")
    #     except jwt.InvalidTokenError:
    #         raise Exception("Invalid token error.")
