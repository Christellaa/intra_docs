from fastapi import FastAPI, Depends
from backend.db.init_db import init_db
from backend.api import user, auth
from backend.crud.auth_crud import check_authentication, get_current_user

app = FastAPI()

init_db()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"], dependencies=[Depends(check_authentication)])
# app.include_router(file.router, prefix="/users/{user_id}/files", tags=["files"])