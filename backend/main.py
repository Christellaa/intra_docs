from fastapi import FastAPI
from backend.api import user
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(user.router, prefix="/files", tags=["files"])