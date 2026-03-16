from pydantic import BaseModel
from core.enum import UserRole
from typing import Optional


class CreateUser(BaseModel):
    name: str
    email: str
    role: UserRole


class ResponseUser(CreateUser):
    id: int

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    name: Optional[str] 
    email: Optional[str]
    role: Optional[UserRole]




