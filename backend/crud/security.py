from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import os
from dotenv import load_dotenv
import uuid
from backend.crud.redis_client import validate_token_not_blacklisted, blacklist_token

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

def refresh_tokens(request: Request, refresh_token: str):
	payload = decode_token(refresh_token)
	if payload.get("type") != "refresh":
		raise HTTPException(status_code=400, detail="Invalid token type")
	validate_token_not_blacklisted(payload.get("jti"))
	access_token = get_token_from_request(request, token_type="access")
	payload_access_token = decode_token(access_token)
	blacklist_token(access_token)
	blacklist_token(refresh_token)
	return create_tokens(payload_access_token.get("sub"), payload_access_token.get("role"))

def create_tokens(sub: str, role: str):
	access_token = create_token(
		data={
			"sub": sub,
			"role": role
		},
		token_type="access"
	)
	refresh_token = create_token(
		data={
			"sub": sub
		},
		token_type="refresh"
	)
	response = JSONResponse(content={"message": "Tokens issued"})
	set_token_cookie(response, access_token, "access_token")
	set_token_cookie(response, refresh_token, "refresh_token")
	return response

def set_token_cookie(response: JSONResponse, token: str, token_name: str):
	response.set_cookie(
		key=token_name,
		value=token,
		# httponly=True,
		# secure=True,
		httponly=False,
		secure=False,
		samesite='Lax'
	)

def create_token(data: dict, token_type: str = "access"):
	to_encode = data.copy()
	now = datetime.now(timezone.utc)
	match token_type:
		case "access":
			expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
		case "refresh":
			expire = now + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
		case _:
			raise ValueError("Invalid token type")
	jti = str(uuid.uuid4())
	payload = {
		**to_encode,
		"exp": expire,
		"jti": jti,
		"iat": now,
		"type": token_type
	}
	return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_refresh_token(request: Request):
	return get_token_from_request(request, token_type="refresh")

def get_token_from_request(request: Request, token_type: str = "access"):
	if token_type == "access":
		token = request.cookies.get("access_token")
	elif token_type == "refresh":
		token = request.cookies.get("refresh_token")
	else:
		raise HTTPException(status_code=400, detail="Invalid token type")
	if token:
		return token
	raise HTTPException(status_code=401, detail="Not authenticated")

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
	type = payload.get("type")
	iat = payload.get("iat")
	if not sub or not jti or not exp or not type or not iat:
		raise HTTPException(status_code=400, detail="Invalid token A structure")
	if type == "access":
		if not role or role not in ["user", "admin"]:
			raise HTTPException(status_code=400, detail="Invalid token B structure")
	if role and type == "refresh":
		raise HTTPException(status_code=400, detail="Invalid token C structure")
	if type not in ["access", "refresh"]:
		raise HTTPException(status_code=400, detail="Invalid token type")