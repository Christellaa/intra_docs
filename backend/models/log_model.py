from sqlalchemy import Column, Integer, JSON, DateTime, func, ForeignKey
from backend.db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as PgEnum
from backend.enums import ActionType, TargetType

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    action = Column(PgEnum(ActionType, name="log_action"), nullable=False)
    target_type = Column(PgEnum(TargetType, name="log_target"), nullable=False)
    target_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="logs")