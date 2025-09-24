from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class FileVisibility(str, Enum):
    PRIVATE = "private"
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"

class FileBase(BaseModel):
    filename: str = Field(..., max_length=255)
    path: str = Field(..., max_length=500)

class FileCreate(FileBase):
    pass

class FileRead(FileBase):
    id: int
    uploaded_at: datetime
    visibility: FileVisibility = FileVisibility.PRIVATE
    user_id: int
    model_config = {"from_attributes": True}