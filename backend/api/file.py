from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas.file_schema import FileCreate, FileRead, FileUpdate
from backend.crud.auth_crud import get_current_user
from backend.db.session import get_db
from backend.crud import file_crud
from backend.crud.log_crud import create_log
from backend.enums import ActionType, TargetType, UserRole, FileVisibility

router = APIRouter()

@router.post("/", response_model=FileRead, status_code=status.HTTP_201_CREATED)
def create_file(user_id: int, file: FileCreate, db: Session = Depends(get_db), User = Depends(get_current_user)):
	if User.id != user_id:
		raise HTTPException(status_code=403, detail="Not authorized to create a file for this user")

	if file_crud.get_file_by_name_and_user(db, filename=file.filename, user_id=user_id):
		raise HTTPException(status_code=409, detail="File with this name already exists for this user")

	db_file = file_crud.create_file(db, user_id=user_id, file=file)
	create_log(db, user_id=user_id, action=ActionType.CREATE, target_type=TargetType.FILE, target_id=db_file.id, details={"filename": db_file.filename})
	return db_file

@router.get("/", response_model=list[FileRead])
def read_files(user_id: int, db: Session = Depends(get_db), User = Depends(get_current_user)):
	if User.id != user_id and User.role != UserRole.ADMIN:
		db_files = file_crud.get_only_public_files_by_user(db, user_id=user_id)
	else:
		db_files = file_crud.get_files_by_user(db, user_id=user_id)
	return db_files

@router.get("/{file_id}", response_model=FileRead)
def read_file(user_id: int, file_id: int, db: Session = Depends(get_db), User = Depends(get_current_user)):
	db_file = file_crud.get_file_by_id_and_user(db, file_id=file_id, user_id=user_id)
	if not db_file:
		raise HTTPException(status_code=404, detail="File not found")

	if db_file.visibility == FileVisibility.PRIVATE and User.id != user_id and User.role != UserRole.ADMIN:
		raise HTTPException(status_code=403, detail="Not authorized to view private files of this user")

	return db_file

@router.put("/{file_id}", response_model=FileRead)
def update_file(user_id: int, file_id: int, file_update: FileUpdate, db: Session = Depends(get_db), User = Depends(get_current_user)):
	if User.id != user_id and User.role != UserRole.ADMIN:
		raise HTTPException(status_code=403, detail="Not authorized to update a file for this user")

	db_file = file_crud.get_file_by_id_and_user(db, file_id=file_id, user_id=user_id)
	if not db_file:
		raise HTTPException(status_code=404, detail="File not found")

	old_filename = db_file.filename
	old_visibility = db_file.visibility
	updated_file = file_crud.update_file(db, db_file=db_file, file_update=file_update)

	details = {}
	if old_filename != updated_file.filename:
		details["old_filename"] = old_filename
		details["new_filename"] = updated_file.filename
	if old_visibility != updated_file.visibility:
		details["old_visibility"] = old_visibility
		details["new_visibility"] = updated_file.visibility
	create_log(db, user_id=user_id, action=ActionType.UPDATE, target_type=TargetType.FILE, target_id=updated_file.id, details=details)
	return updated_file

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(user_id: int, file_id: int, db: Session = Depends(get_db), User = Depends(get_current_user)):
	if User.id != user_id and User.role != UserRole.ADMIN:
		raise HTTPException(status_code=403, detail="Not authorized to delete a file for this user")

	db_file = file_crud.get_file_by_id_and_user(db, file_id=file_id, user_id=user_id)
	if not db_file:
		raise HTTPException(status_code=404, detail="File not found")

	create_log(db, user_id=user_id, action=ActionType.DELETE, target_type=TargetType.FILE, target_id=file_id, details={"filename": db_file.filename})
	db.delete(db_file)
	db.commit()
	return