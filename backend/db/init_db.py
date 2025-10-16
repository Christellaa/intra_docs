from backend.db.base import Base
from backend.db.session import engine
from backend.models import user_model, file_model, log_model
from backend.enums import UserRole
from backend.db.session import SessionLocal

def create_admin_user(db):
    from backend.crud import user_crud
    from backend.schemas.user_schema import UserCreate

    existing_admin = db.query(user_crud.User).filter(user_crud.User.role == UserRole.ADMIN).first()
    if existing_admin:
        return

    admin_data = UserCreate(
        first_name="Admin first name",
        last_name="Admin last name",
        password="admin",
        confirm_password="admin",
        role=UserRole.ADMIN
    )
    return user_crud.create_user(db, admin_data)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        create_admin_user(db)
    finally:
        db.close()