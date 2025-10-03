from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.schemas.user_schema import UserRead
from backend.db.session import get_db
from backend.crud import auth_crud
from fastapi.security import OAuth2PasswordRequestForm
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = auth_crud.authenticate_user(db, form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
		)
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = auth_crud.create_access_token(
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

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
	return {"msg": "Logout successful"}



# envoiyer token dans un cookie httpOnly
# suppression du token lors du logout coté client + blacklist du token coté serveur?
# gestion des refresh token
# gestion des permissions (admin, user) quand on charge les routes: on verif presence + validite du token dans les headers, puis si c'est un admin ou user