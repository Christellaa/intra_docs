from http.client import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.crud.user_crud import get_user_by_username
from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv
from backend.db.session import get_db
from fastapi import Request, Depends

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_pwd(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_pwd(password, user.hashed_password):
        return False
    return user

def get_token_from_request(request: Request):
    # token = request.cookies.get("access_token") // for cookie-based auth
    auth: str = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        return auth.split(" ")[1]
    return None

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = get_token_from_request(request)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def check_authentication(request: Request):
    token = get_token_from_request(request)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")