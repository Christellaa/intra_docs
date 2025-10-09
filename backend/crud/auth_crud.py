from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.db.session import get_db
from backend.crud.user_crud import get_user_by_username
from backend.crud.security import get_token_from_request, decode_token
from backend.crud.redis_client import validate_token_not_blacklisted

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

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = get_token_from_request(request)
    payload = decode_token(token)
    validate_token_not_blacklisted(payload.get("jti"))
    username: str = payload.get("sub")
    user = get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_admin(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

def check_authentication(request: Request):
    token = get_token_from_request(request)
    decode_token(token)