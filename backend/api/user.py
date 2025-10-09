from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.models.user_model import User
from backend.schemas.user_schema import UserCreate, UserRead, UserUpdate
from backend.db.session import get_db
from backend.crud import user_crud, auth_crud

router = APIRouter()
public_router = APIRouter()

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_crud.get_current_user)):
    user = user_crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user")
    return current_user

@router.get("/", response_model=list[UserRead], dependencies=[Depends(auth_crud.get_current_user)])
def read_users(search: str | None = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, search=search, skip=skip, limit=limit)
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users

@public_router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = user_crud.create_user(db, user)
    return new_user

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth_crud.get_current_user)):
    db_user = user_crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_crud.update_user(db=db, db_user=db_user, user=user, current_user=current_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth_crud.get_current_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()