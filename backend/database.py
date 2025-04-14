# Description: This file contains the database connection and session creation logic.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Initialize Metadata and Base
load_dotenv()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide session to request
    finally:
        db.close()  # Ensure session is closed after request

def db_connect():

    DATABASE_URL = os.getenv("DATABASE_URL")

    try:
        # Create the database engine
        engine = create_engine(DATABASE_URL)
        print("Database connection established.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise e
    
    return engine

engine = db_connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
    
