from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Book
from schema import BookSchema
from supabase_client import supabase
from pydantic import BaseModel
from typing import Optional
from auth.dependencies import require_role

router = APIRouter()

class UpdateBookSchema(BaseModel):
    book_title: Optional[str] = None
    author: Optional[str] = None
    year_published: Optional[str] = None
    copies_available: Optional[int] = None

"""
Query all books
"""
@router.get("/books")
def get_books(db: Session = Depends(get_db)):
    try:
        books = supabase.table("books").select("*").execute()
        return books.data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching books from Supabase")

"""
Query books by title, author, or year published
"""
@router.get("/books/search")
def search_books(
    book_title: str = None,
    author_name: str = None,
    year_published: str = None,
    db: Session = Depends(get_db),
):
    try:
        query = supabase.table("books").select("*")

        if book_title:
            query = query.eq("book_title", book_title)
        if author_name:
            query = query.eq("author_name", author_name)
        if year_published:
            query = query.eq("year_published", year_published)

        books = query.execute()
        return books.data
    except Exception as e:
        print("Error fetching books: ", e)
        raise HTTPException(status_code=500, detail="Error fetching books from Supabase")

"""
Query a single book by ID
"""
@router.get("/books/{book_id}")
def get_books_by_id(book_id: str, db:Session = Depends(get_db)):
    try:
        book = supabase.table("books").select("*").eq("book_id", book_id).single().execute()
        if not book.data:
            raise HTTPException(status_code=404, detail="Book not found")
        return book.data
    except Exception as e:
        print("Error fetching book: ", e)
        raise HTTPException(status_code=500, detail="Error fetching book from Supabase")

"""
Create a new book
This is for admin roles only (for implementing RBAC later)
"""
@router.post("/books", dependencies=[Depends(require_role("admin"))])
def create_book(book: BookSchema):
    try:
        response = supabase.table("books").insert(book.dict()).execute()
        return response.data
    except Exception as e:
        print("❌ Insert error:", e)
        raise HTTPException(status_code=500, detail="Could not insert book")

    print("Book inserted successfully!")

"""
Update a book by ID
This is for admin roles only (for implementing RBAC later)
"""
@router.put("/books/{book_id}")
def update_book_by_idk(book_id: str, book: UpdateBookSchema):
    try:
        update_data = {key: value for key, value in book.dict().items() if value is not None}

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")
        
        response = supabase.table("books").update(update_data).eq("book_id", book_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Book not found")

        return response.data
    except Exception as e:
        print("❌ Update error:", e)
        raise HTTPException(status_code=500, detail="Could not update book")