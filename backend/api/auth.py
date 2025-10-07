from fastapi import APIRouter, Depends, HTTPException, status
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
	user = auth_crud.authenticate_user(db, form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
		)
	response = security.create_access_token(user)
	return response

@router.post("/logout")
def logout(request: str = Depends(security.get_token_from_request)):
	blacklist_token(request)
	response = JSONResponse(content={"message": "Logout successful"})
	response.delete_cookie("access_token")
	return response

# gestion des refresh token
# gestion des permissions (admin, user) quand on charge les routes: on verif presence + validite du token dans les headers, puis si c'est un admin ou user