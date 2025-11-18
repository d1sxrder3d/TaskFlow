from pydantic import BaseModel, Field
from typing import Optional



class TagBase(BaseModel):
    name: str = Field(..., max_length=50)
    color: str = Field(..., max_length=20)
    project_id: int

class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=20)
    project_id: Optional[int] = None


class TagRead(TagBase):
    id: int
    class Config:
        orm_mode = True
