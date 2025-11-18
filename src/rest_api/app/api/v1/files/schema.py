from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum



class FileStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class FileBase(BaseModel):
    name: str = Field(..., max_length=50)
    size: int
    mime_type: str = Field(..., max_length=100)
    original_name: str = Field(..., max_length=255)
    status: FileStatus = FileStatus.UPLOADED
    s3_path: str = Field(..., max_length=255)
    project_id: int
    user_id: Optional[int] = None


class FileCreate(FileBase):
    pass


class FileUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    status: Optional[FileStatus] = None
    s3_path: Optional[str] = Field(None, max_length=255)


class FileRead(FileBase):
    id: int
    class Config:
        from_attributes = True

