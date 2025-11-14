from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict




class UserUpdateRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserListResponse(BaseModel):

    users: list[UserResponse]
    total: int

