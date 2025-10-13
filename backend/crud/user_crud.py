from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.models.user_model import User
from backend.schemas.user_schema import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(pwd: str) -> str:
    return pwd_context.hash(pwd)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, search: str | None = None, skip: int = 0, limit: int = 10):
    query = db.query(User)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (User.username.ilike(search_term)) |
            (User.first_name.ilike(search_term)) |
            (User.last_name.ilike(search_term))
        )
    return query.order_by(User.id.asc()).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_pwd = hash_pwd(user.password)
    db_user = User(
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, user: UserUpdate, current_user: User):
    if user.first_name is not None and user.first_name != db_user.first_name:
        db_user.first_name = user.first_name
    if user.last_name is not None and user.last_name != db_user.last_name:
        db_user.last_name = user.last_name
    if user.role is not None and user.role != db_user.role and user.role in ["admin", "user"]:
        if current_user.id == db_user.id and current_user.role == "admin":
            raise HTTPException(status_code=403, detail="Admin users cannot change their own role")
        db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user