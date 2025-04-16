from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schema import UserSchema
from supabase_client import supabase

router = APIRouter()

"""
These routes are accessible to all roles.
"""

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    """
    Get all users from the database.
    """
    try:
        response = supabase.table("users").select("*").execute()
    except Exception as e:
        print("Error fetching users: ", e)
        raise HTTPException(status_code=500, detail="Error Fetching Users from Supabase")
    return response.data

@router.post("/users", response_model=UserSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    try:
        response = supabase.table("users").insert(user.dict()).execute()
    except Exception as e:
        print("Error creating user: ", e)
        raise HTTPException(status_code=500, detail="Error Creating User in Supabase")

    # Ensure response.data is not empty and return the first item
    if response.data:
        return response.data[0]
    else:
        raise HTTPException(status_code=500, detail="Failed to create user.")