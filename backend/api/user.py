from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.models.user_model import User
from backend.schemas.user_schema import UserCreate, UserRead, UserUpdate
from backend.db.session import get_db
from backend.crud import user_crud, auth_crud
from backend.crud.log_crud import create_log
from backend.enums import ActionType, TargetType

router = APIRouter()

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_crud.get_current_user)):
    user = user_crud.get_user_by_id(db=db, user_id=user_id)
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

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_crud.get_current_admin)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = user_crud.create_user(db, user)
    create_log(db, user_id=current_user.id, action=ActionType.CREATE, target_type=TargetType.USER, target_id=new_user.id, details={"username": new_user.username})
    return new_user

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth_crud.get_current_admin)):
    db_user = user_crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    old_first_name = db_user.first_name
    old_last_name = db_user.last_name
    old_role = db_user.role
    updated_user = user_crud.update_user(db=db, db_user=db_user, user=user, current_user=current_user)

    details = {}
    if old_first_name != updated_user.first_name:
        details["old_first_name"] = old_first_name
        details["new_first_name"] = updated_user.first_name
    if old_last_name != updated_user.last_name:
        details["old_last_name"] = old_last_name
        details["new_last_name"] = updated_user.last_name
    if old_role != updated_user.role:
        details["old_role"] = old_role
        details["new_role"] = updated_user.role
    details["username"] = updated_user.username
    create_log(db, user_id=current_user.id, action=ActionType.UPDATE, target_type=TargetType.USER, target_id=user_id, details=details)
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_crud.get_current_admin)):
    user = user_crud.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    create_log(db, user_id=current_user.id, action=ActionType.DELETE, target_type=TargetType.USER, target_id=user_id, details={"username": user.username})
    db.delete(user)
    db.commit()