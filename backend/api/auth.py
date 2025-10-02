from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.schemas.user_schema import UserRead
from backend.db.session import get_db
from backend.crud import auth_crud
from fastapi.security import OAuth2PasswordRequestForm
import os
from dotenv import load_dotenv

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
	access_token = auth_crud.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
	
	return {"msg": "Login successful", "user": UserRead.from_orm(user), "access_token": access_token, "token_type": "bearer"}

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
	return {"msg": "Logout successful"}