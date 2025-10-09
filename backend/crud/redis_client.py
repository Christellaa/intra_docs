import redis
from fastapi import HTTPException
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import time

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
PORT_REDIS = int(os.getenv("PORT_REDIS"))
r = redis.Redis(host=REDIS_HOST, port=PORT_REDIS, db=0, decode_responses=True)

def blacklist_token(token: str):
	from backend.crud.auth_crud import decode_token
	payload = decode_token(token)
	jti = payload.get("jti")
	exp = payload.get("exp")
	ttl = exp - int(datetime.now(timezone.utc).timestamp())
	if ttl > 0:
		r.setex(name=f"blacklist:{jti}", time=ttl, value="1")
		time.sleep(0.1)

def validate_token_not_blacklisted(jti: str):
    if jti and r.get(f"blacklist:{jti}"):
        raise HTTPException(status_code=401, detail="Token has been revoked")