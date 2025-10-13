from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas.file_schema import FileCreate, FileRead, FileUpdate
from backend.crud.auth_crud import get_current_user
from backend.db.session import get_db
from backend.crud import file_crud

router = APIRouter()

@router.post("/", response_model=FileRead, status_code=status.HTTP_201_CREATED)
def create_file(user_id: int, file: FileCreate, db: Session = Depends(get_db), User = Depends(get_current_user)):
	if User.id != user_id and User.role != "admin":
		raise HTTPException(status_code=403, detail="Not authorized to create a file for this user")
	if file_crud.get_file_by_name_and_user(db, filename=file.filename, user_id=user_id):
		raise HTTPException(status_code=409, detail="File with this name already exists for this user")
	db_file = file_crud.create_file(db, user_id=user_id, file=file)
	return db_file

@router.get("/", response_model=list[FileRead])
def read_files(user_id: int, db: Session = Depends(get_db), User = Depends(get_current_user)):
	if User.id != user_id and User.role != "admin":
		db_files = file_crud.get_only_public_files_by_user(db, user_id=user_id)
	else:
		db_files = file_crud.get_files_by_user(db, user_id=user_id)
	return db_files

@router.get("/{file_id}", response_model=FileRead)
def read_file(user_id: int, file_id: int, db: Session = Depends(get_db), User = Depends(get_current_user)):
	db_file = file_crud.get_file_by_id_and_user(db, file_id=file_id, user_id=user_id)
	if not db_file:
		raise HTTPException(status_code=404, detail="File not found")
	if db_file.visibility == "private" and User.id != user_id and User.role != "admin":
		raise HTTPException(status_code=403, detail="Not authorized to view private files of this user")
	return db_file

@router.put("/{file_id}", response_model=FileRead)
def update_file(user_id: int, file_id: int, file_update: FileUpdate, db: Session = Depends(get_db), User = Depends(get_current_user)):
	if User.id != user_id and User.role != "admin":
		raise HTTPException(status_code=403, detail="Not authorized to update a file for this user")
	db_file = file_crud.get_file_by_id_and_user(db, file_id=file_id, user_id=user_id)
	if not db_file:
		raise HTTPException(status_code=404, detail="File not found")
	return file_crud.update_file(db, db_file=db_file, file_update=file_update)

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(user_id: int, file_id: int, db: Session = Depends(get_db), User = Depends(get_current_user)):
	if User.id != user_id and User.role != "admin":
		raise HTTPException(status_code=403, detail="Not authorized to delete a file for this user")
	db_file = file_crud.get_file_by_id_and_user(db, file_id=file_id, user_id=user_id)
	if not db_file:
		raise HTTPException(status_code=404, detail="File not found")
	db.delete(db_file)
	db.commit()
	return