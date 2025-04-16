from fastapi import FastAPI
from router import books, users, user_auth, genre
from database import Base, engine 

app = FastAPI()

app.include_router(books)
app.include_router(users)
app.include_router(user_auth, prefix="/auth")
app.include_router(genre)

print("🚀 Starting FastAPI application...")