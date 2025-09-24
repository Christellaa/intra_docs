from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.models.user_model import User
from backend.schemas.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_pwd(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)

def get_hashed_pwd(pwd: str) -> str:
    return pwd_context.hash(pwd)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    hashed_pwd = get_hashed_pwd(user.password)
    db_user = User(
        username = user.username,
        email=user.email,
        hashed_password=hashed_pwd,
        img_path=user.img_path,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user