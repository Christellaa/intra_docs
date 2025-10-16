from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas.log_schema import LogRead
from backend.crud.auth_crud import get_current_user
from backend.db.session import get_db
from backend.crud import log_crud

router = APIRouter()

@router.get("/", response_model=list[LogRead])
def read_logs(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), User = Depends(get_current_user)):
	return log_crud.read_logs(user_id=user_id, db=db, skip=skip, limit=limit, user=User)