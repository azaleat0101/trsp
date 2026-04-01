from fastapi import FastAPI

from .models import UserCreate
from . import products, auth_simple, auth_signed, headers_handlers

app = FastAPI()

@app.post("/create_user")
def create_user(user: UserCreate):
    return user

app.include_router(products.router)
app.include_router(auth_simple.router)
app.include_router(auth_signed.router)
app.include_router(headers_handlers.router)