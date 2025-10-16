from pydantic import BaseModel, ConfigDict
from datetime import datetime
from backend.enums import ActionType, TargetType

class LogRead(BaseModel):
    id: int
    action: ActionType
    target_type: TargetType
    target_id: int | None = None
    # target_name: str
    details: dict | None = None
    user_id: int
    timestamp: datetime

    model_config = ConfigDict(extra="forbid")