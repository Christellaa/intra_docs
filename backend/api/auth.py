from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.crud import auth_crud
from backend.crud import security
from backend.crud.redis_client import blacklist_token

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	# check not already logged in
	user = auth_crud.authenticate_user(db, form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
		)
	response = security.create_tokens(user.username, user.role)
	return response

@router.post("/logout")
def logout(access_token: str = Depends(security.get_token_from_request)):
	blacklist_token(access_token)
	refresh_token = security.get_refresh_token()
	blacklist_token(refresh_token)
	response = JSONResponse(content={"message": "Logout successful"})
	response.delete_cookie("access_token")
	response.delete_cookie("refresh_token")
	return response

@router.post("/refresh")
def refresh(request: Request, token: str = Depends(security.get_refresh_token)):
	response = security.refresh_tokens(request, token)
	return response

# gestion des refresh token:
# a chaque appel de /refresh -> verif si refresh token n'est pas expiré et que son iat + max durée n'est pas depassée -> donc qu'il est pas blacklisté (redis)
# si ok -> on genere un nouveau access token + refresh token + on blacklist l'ancien refresh token
# si pas ok -> erreur 401 + l'user doit se relog

# gestion des permissions (admin, user) quand on charge les routes: on verif presence + validite du token dans les headers, puis si c'est un admin ou user