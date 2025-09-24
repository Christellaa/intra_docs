from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from backend.db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as PgEnum
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    img_path = Column(String(255), nullable=True)
    role = Column(PgEnum(UserRole, name="user_role", create_type=True), default=UserRole.USER.value, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    files = relationship("File", back_populates="user", cascade="all, delete-orphan")
