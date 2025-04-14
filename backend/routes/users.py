from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import UserDetail
from schema import UserDetailSchema
from supabase_client import supabase

router = APIRouter()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    """
    Get all users from the database.
    """
    response = supabase.table("users").select("*").execute()
    return response.data