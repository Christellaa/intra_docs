import redis
from fastapi import HTTPException
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
PORT_REDIS = int(os.getenv("PORT_REDIS"))
r = redis.Redis(host=REDIS_HOST, port=PORT_REDIS, db=0, decode_responses=True)

def blacklist_token(request):
	from backend.crud.auth_crud import decode_token
	payload = decode_token(request)
	jti = payload.get("jti")
	exp = payload.get("exp")
	ttl = exp - int(datetime.now(timezone.utc).timestamp())
	if ttl > 0:
		r.setex(name=f"blacklist:{jti}", time=ttl, value="1")

def is_token_blacklisted(payload: dict):
    jti = payload.get("jti")
    if jti and r.get(f"blacklist:{jti}"):
        raise HTTPException(status_code=401, detail="Token has been revoked")
    return False