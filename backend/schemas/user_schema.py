from pydantic import BaseModel, EmailStr, ConfigDict, model_validator, field_validator
from datetime import datetime
from backend.enums import UserRole, UserStatus

class UserBase(BaseModel):
    first_name: str
    last_name: str
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE

class UserCreate(UserBase):
    password: str
    confirm_password: str
    username: str | None = None  # auto-generated
    email: EmailStr | None = None  # auto-generated

    @model_validator(mode='after')
    @classmethod
    def check_passwords_match(cls, model: 'UserCreate') -> 'UserCreate':
        if model.password != model.confirm_password:
            raise ValueError("Passwords do not match")
        return model

    @model_validator(mode='before')
    @classmethod
    def set_username_and_email(cls, values: dict) -> dict:
        first_name = values.get('first_name').strip().lower()
        last_name = values.get('last_name').strip().lower()
        if first_name and last_name:
            username = f"{first_name[0]}{last_name[:5]}"
            values['username'] = username
            values['email'] = f"{username}@intra-docs.com"
        return values

    @model_validator(mode='before')
    @classmethod
    def forbid_username_email(cls, values: dict) -> dict:
        if 'username' in values or 'email' in values:
            raise ValueError("Username and email are auto-generated and cannot be provided")
        return values

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, value: str) -> str:
        if len(value.strip()) < 2:
            raise ValueError("Must be at least 2 non-whitespace characters")
        if len(value.strip()) > 50:
            raise ValueError("Must be at most 50 characters")
        value = value.strip()
        return value

    model_config = ConfigDict(extra="forbid")

class UserRead(UserBase):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    role: UserRole
    status: UserStatus

    model_config = ConfigDict(extra="forbid", from_attributes=True)

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    role: UserRole | None = None

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, value: str) -> str:
        if len(value.strip()) < 2:
            raise ValueError("Must be at least 2 non-whitespace characters")
        if len(value.strip()) > 50:
            raise ValueError("Must be at most 50 characters")
        value = value.strip()
        return value
    
    # TODO: modify username and email if first_name or last_name is updated

    model_config = ConfigDict(extra="forbid")