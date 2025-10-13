from backend.models.file_model import File

def create_file(db, user_id, file):
	db_file = File(
		filename=file.filename,
		path=file.path,
		visibility=file.visibility,
		user_id=user_id
	)
	db.add(db_file)
	db.commit()
	db.refresh(db_file)
	return db_file

def get_file_by_name_and_user(db, filename, user_id):
	return db.query(File).filter(File.filename == filename, File.user_id == user_id).first()

def get_file_by_id_and_user(db, file_id, user_id):
	return db.query(File).filter(File.id == file_id, File.user_id == user_id).first()

def get_only_public_files_by_user(db, user_id):
	return db.query(File).filter(File.user_id == user_id, File.visibility == "public").all()

def get_files_by_user(db, user_id):
	return db.query(File).filter(File.user_id == user_id).all()

def update_file(db, db_file, file_update):
	if file_update.filename is not None and file_update.filename != db_file.filename:
		db_file.filename = file_update.filename
	if file_update.visibility is not None and file_update.visibility != db_file.visibility:
		db_file.visibility = file_update.visibility
	db.commit()
	db.refresh(db_file)
	return db_file