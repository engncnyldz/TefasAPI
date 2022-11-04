from dataclasses import replace
from fastapi import FastAPI
from .routers import funds

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to TefasAPI !"}

app.include_router(funds.router)
