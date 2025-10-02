from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.crud.user_crud import get_user_by_username

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_pwd(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_pwd(password, user.hashed_password):
        return False
    return user