from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    name: str
