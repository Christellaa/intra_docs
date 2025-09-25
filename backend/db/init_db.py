from backend.db.base import Base
from backend.db.session import engine
from backend.models import user_model, file_model

def init_db():
    Base.metadata.create_all(bind=engine)