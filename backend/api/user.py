from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.schemas.user_schema import UserCreate, UserRead
from backend.db.session import get_db
from backend.crud import user_crud

router = APIRouter()

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = user_crud.get_user(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserRead])
def read_users(search: str | None = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        users = user_crud.get_users(db, search=search, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Users not found")
    return users

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = user_crud.create_user(db, user)
    return new_user