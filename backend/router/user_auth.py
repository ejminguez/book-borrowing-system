from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests
from supabase import create_client, Client
from sqlalchemy .orm import Session
from database import get_db
from auth.dependencies import verify_token
import jwt

load_dotenv()
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
JWT_ALGORITHM = "HS256"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

security = HTTPBearer()

# Define the sign-in request model
class SignInRequest(BaseModel):
    email: str
    password: str

# Define the sign-up request model
class SignUpRequest(BaseModel):
    email: str
    password: str

class OnboardPayload(BaseModel):
    username: str

router = APIRouter()

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
            "Authorization": f"Bearer {SUPABASE_JWT_SECRET}",
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

@router.post("/onboard")
def onboard_user(data: OnboardPayload, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Log the token for debugging
        print("Token received:", token)

        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload["sub"]  # Assuming 'sub' is the unique user ID in the JWT token
        email = payload["email"]

        # Check if the user is already onboarded
        existing = supabase.table("users").select("user_id").eq("user_id", user_id).execute()
        if existing.data:
            return {"message": "User already onboarded."}

        # Insert the user into the 'users' table
        supabase.table("users").insert({
            "user_id": user_id,
            "email": email,
            "username": data.username,  # Getting the username from the request payload
            "role": "reader"  # Assign default role, could be customized
        }).execute()

        return {"message": "User onboarded successfully."}
    except jwt.PyJWTError as e:
        print("Error decoding token:", str(e))  # Log the error for debugging
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Onboarding failed: {e}")