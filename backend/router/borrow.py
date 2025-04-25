from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Book
from schema import BookSchema
from supabase_client import supabase
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
