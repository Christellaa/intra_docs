from sqlalchemy.orm import Session
from backend.models.log_model import Log
from backend.models.file_model import File
from backend.crud.user_crud import get_user_by_id
from fastapi import HTTPException
from backend.enums import UserRole, FileVisibility, TargetType

def read_logs(user_id: int, db: Session, skip: int = 0, limit: int = 10, user = None):
	target = get_user_by_id(db, user_id)
	if not target:
		raise HTTPException(status_code=404, detail="User not found")
	query = db.query(Log).outerjoin(File, Log.target_id == File.id).filter(Log.user_id == user_id)
	if user.role != UserRole.ADMIN and user.id != user_id:
		query = query.filter((Log.target_type != TargetType.FILE) | (File.id == None) | (File.visibility != FileVisibility.PRIVATE))
	return query.order_by(Log.timestamp.desc()).offset(skip).limit(limit).all()

def create_log(db: Session, user_id: int, action: str, target_type: str, target_id: int | None = None, details: dict | None = None):
	new_log = Log(
		user_id=user_id,
		action=action,
		target_type=target_type,
		target_id=target_id,
		details=details,
	)
	db.add(new_log)
	db.commit()
	db.refresh(new_log)