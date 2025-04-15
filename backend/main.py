from fastapi import FastAPI
from router import books, users, user_auth
from database import Base, engine 

app = FastAPI()

app.include_router(books)
app.include_router(users)
app.include_router(user_auth, prefix="/auth")

print("🚀 Starting FastAPI application...")