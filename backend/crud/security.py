from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_access_token(user):
	access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
	access_token = create_token(
		data={"sub": user.username, "role": user.role},
		expires_delta=access_token_expires
	)
	response = JSONResponse(content={"message": "Login successful"})
	response.set_cookie(
		key="access_token",
		value=access_token,
		# httponly=True,
		# secure=True,
		httponly=False,
		secure=False,
		samesite='Lax'
	)
	return response

def create_token(data: dict, expires_delta: timedelta | None = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	jti = str(uuid.uuid4())
	to_encode.update({"exp": expire, "jti": jti})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

def get_token_from_request(request: Request):
	# token = request.cookies.get("access_token") // for cookie-based auth
	auth: str = request.headers.get("Authorization")
	if auth and auth.startswith("Bearer "):
		return auth.split(" ")[1]
	raise HTTPException(status_code=401, detail="Not authenticated") # not useful but need for checks from functions calling this one

def decode_token(token: str):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		validate_token_structure(payload)
		return payload
	except ExpiredSignatureError:
		raise HTTPException(status_code=401, detail="Token has expired")
	except JWTError:
		raise HTTPException(status_code=400, detail="Invalid token")
	
def validate_token_structure(payload: dict):
	sub = payload.get("sub")
	role = payload.get("role")
	jti = payload.get("jti")
	exp = payload.get("exp")
	if not sub or not role or not jti or not exp:
		raise HTTPException(status_code=400, detail="Invalid token structure")