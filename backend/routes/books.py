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
        return books.data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching books from Supabase")

@router.get("/books/{book_id}")
def get_books_by_id(book_id: str, db:Session = Depends(get_db)):
    """
    Get a book by its ID.
    """
    try:
        book = supabase.table("books").select("*").eq("book_id", book_id).single().execute()
        if not book.data:
            raise HTTPException(status_code=404, detail="Book not found")
        return book.data
    except Exception as e:
        print("Error fetching book: ", e)
        raise HTTPException(status_code=500, detail="Error fetching book from Supabase")