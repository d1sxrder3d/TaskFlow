from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., description="Username или email")
    password: str = Field(..., min_length=8)


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str

