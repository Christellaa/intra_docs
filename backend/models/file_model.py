from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Boolean
from backend.db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as PgEnum
from backend.enums import FileVisibility

class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    path = Column(String(500), nullable=False)
    visibility = Column(PgEnum(FileVisibility, name="file_visibility", create_type=True), default=FileVisibility.PRIVATE.value, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="files")


