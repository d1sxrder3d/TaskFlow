from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    username: str = Field(..., description="Username или email")
    password: str = Field(..., min_length=8)


class RegisterRequest(BaseModel):

    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr

    password: str = Field(..., min_length=8, max_length=128)

    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str

