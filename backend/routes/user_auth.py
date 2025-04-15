from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
from models import UserDetail
from supabase_client import supabase

router = APIRouter()

