from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests
from supabase import create_client, Client

router = APIRouter()

# Load environment variables from the .env file
load_dotenv()
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Define the sign-in request model
class SignInRequest(BaseModel):
    email: str
    password: str

# Define the sign-up request model
class SignUpRequest(BaseModel):
    email: str
    password: str


"""
These routes are accessible to all roles.
"""

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
def sign_up(data: SignUpRequest):
    auth_response = requests.post(
        f"{SUPABASE_URL}/auth/v1/signup",
        headers={
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"  # Optional but recommended
        },
        json={
            "email": data.email,
            "password": data.password,
        }
    )

    print("Auth Status Code:", auth_response.status_code)
    print("Auth Response JSON:", auth_response.json())

    if auth_response.status_code != 200:
        raise HTTPException(status_code=400, detail=auth_response.json())

    print("Signed up successfully.")
    raise HTTPException(status_code=200, detail="User signed up successfully")

"""
Checks if user is signed up and returns user data.
"""
