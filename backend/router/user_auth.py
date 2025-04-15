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
    username: str
    role: str

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
    # Step 1: Create user via Supabase Auth
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

    auth_json = auth_response.json()
    user_id = auth_json.get("id")  # Because it's at the top level

    if not user_id:
        raise HTTPException(status_code=500, detail="Failed to retrieve user ID after signup.")

    """
    Bug: Permission denied when inserting into public.users
    Sign up is successful, but inserting into public.users fails with permission denied error.
    """
    # Step 2: Insert into public.users using supabase-py client
    try:
        response = supabase.table("users").insert({
            "user_id": user_id,
            "username": data.username,
            "email": data.email,
            "is_active": True,
            "role": data.role
        }).execute()
    except Exception as e:
        print("Insert Error:", e)
        raise HTTPException(status_code=500, detail="Error inserting user profile into public.users")

    return {"message": "User successfully registered 🎉", "user_id": user_id}