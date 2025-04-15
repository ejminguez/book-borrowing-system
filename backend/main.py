# This file initializes the FastAPI App
from fastapi import FastAPI
from routes import books, users
from database import Base, engine 

app = FastAPI()
app.include_router(books)
app.include_router(users)

print("🚀 Starting FastAPI application...")