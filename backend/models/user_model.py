from sqlalchemy import Column, Integer, String, DateTime, func
from backend.db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as PgEnum
from backend.enums import UserRole, UserStatus

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(PgEnum(UserRole, name="user_role", create_type=True), default=UserRole.USER.value, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(PgEnum(UserStatus, name="user_status", create_type=True), default=UserStatus.ACTIVE.value, nullable=False)

    files = relationship("File", back_populates="user", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="user", cascade="all, delete-orphan")