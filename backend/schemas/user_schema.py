from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str
    img_path: Optional[str] = None

class UserRead(UserBase):
    id: int
    created_at: datetime
    img_path: Optional[str] = None

    model_config = {"from_attributes": True}