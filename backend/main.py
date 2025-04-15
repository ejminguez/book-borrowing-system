# This file initializes the FastAPI App
from fastapi import FastAPI
from routes import books
from database import Base, engine 

app = FastAPI()
app.include_router(books)

print("🚀 Starting FastAPI application...")