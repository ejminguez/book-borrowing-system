from fastapi import FastAPI
from router import books, users
from database import Base, engine 

app = FastAPI()

app.include_router(books)
app.include_router(users)

print("🚀 Starting FastAPI application...")