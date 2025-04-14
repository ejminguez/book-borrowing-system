from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Book
from schema import BookSchema
from supabase_client import supabase

router = APIRouter()

@router.get("/books")
def get_books(db: Session = Depends(get_db)):
    """
    Get all books from the database.
    """
    try:
        books = supabase.table("books").select("*").execute()
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching books from Supabase")