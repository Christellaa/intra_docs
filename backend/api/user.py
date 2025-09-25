from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.schemas.user_schema import UserCreate, UserRead
from backend.db.session import get_db
from backend.crud import user_crud

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = user_crud.create_user(db, user)
    return new_user

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = user_crud.get_user(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")
    return user