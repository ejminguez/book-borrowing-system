# This file initializes the FastAPI App
from fastapi import FastAPI
from models import *
from database import engine, Base

app = FastAPI()

# Create the database tables if they don't exist
print("🚀 Attempting to create tables in Supabase...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")