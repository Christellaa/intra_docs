from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum
from backend.schemas.user_schema import UserRead

class FileVisibility(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"

class FileBase(BaseModel):
    filename: str = Field(..., max_length=255)
    path: str = Field(..., max_length=500)
    visibility: FileVisibility = FileVisibility.PRIVATE

class FileCreate(FileBase):
    pass

    model_config = ConfigDict(extra="forbid")

class FileRead(FileBase):
    id: int
    uploaded_at: datetime
    # user_id: int
    user: UserRead

    model_config = ConfigDict(extra="forbid", from_attributes=True)

class FileUpdate(BaseModel):
    filename: str | None = Field(None, max_length=255)
    visibility: FileVisibility | None = None

    model_config = ConfigDict(extra="forbid")