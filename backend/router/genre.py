from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Genre
from schema import GenreSchema
from supabase_client import supabase

router = APIRouter()

@router.get("/genres")
def get_genres(db: Session = Depends(get_db)):
    try:
        genres = supabase.table("genres").select("*").execute()
        return genres.data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching genres from Supabase")
    
    raise HTTPException(status_code=200, detail="Genres fetched successfully")

@router.post("/genres")
def create_genre(genre: GenreSchema):
    try:
        response = supabase.table("genres").insert(genre.dict()).execute()
        return response.data
    except Exception as e:
        print("❌ Insert error:", e)
        raise HTTPException(status_code=500, detail="Could not insert genre")
    
    print("Genre inserted successfully!")
    raise HTTPException(status_code=200, detail="Genre inserted successfully")