from fastapi import APIRouter, HTTPException
from database import get_db
from pydantic import BaseModel
from supabase_client import supabase
import os
from dotenv import load_dotenv
import requests
from schema import UserSchema

router = APIRouter()
load_dotenv()
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

class SignInRequest(BaseModel):
    email: str
    password: str

@router.post("/signin")
def sign_in(data: SignInRequest):
    response = requests.post(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        headers={
            "apikey": SUPABASE_KEY,
            "Content-Type": "application/json",
        },
        json={"email": data.email, "password": data.password}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return response.json()  # returns access_token, user, etc.


@router.post("/signup")
def sign_up(data: UserSchema):
    response = requests.post(
        f"{SUPABASE_URL}/auth/v1/signup",
        headers={
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Content-Type": "application/json",
        },
        json={
            "email": data.email,
            "password": data.password,
            "data": { 
                "username": data.username,
                "is_active": True,
                "role": data.role
             }  # attaches to user_metadata
        }
    )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Signup failed")

    return response.json()
