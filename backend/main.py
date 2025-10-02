from fastapi import FastAPI
from backend.db.init_db import init_db
from backend.api import user, auth

app = FastAPI()

init_db()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
# app.include_router(file.router, prefix="/users/{user_id}/files", tags=["files"])