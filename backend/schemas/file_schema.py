from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from backend.schemas.user_schema import UserRead
from backend.enums import FileVisibility

class FileBase(BaseModel):
    filename: str = Field(..., max_length=255)
    path: str = Field(..., max_length=500)
    visibility: FileVisibility = FileVisibility.PRIVATE

class FileCreate(FileBase):
    model_config = ConfigDict(extra="forbid")
    pass

class FileRead(FileBase):
    id: int
    uploaded_at: datetime
    user: UserRead

    model_config = ConfigDict(extra="forbid", from_attributes=True)

class FileUpdate(BaseModel):
    filename: str | None = Field(None, max_length=255)
    visibility: FileVisibility | None = None

    model_config = ConfigDict(extra="forbid")