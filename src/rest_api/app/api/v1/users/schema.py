from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    first_name: str | None = None
    last_name: str | None = None

    is_active: bool = True
    is_superuser: bool = False

    class Config:
        orm_mode = True