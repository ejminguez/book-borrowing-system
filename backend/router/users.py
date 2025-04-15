from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schema import UserSchema
from supabase_client import supabase

router = APIRouter()

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
