from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
JWT_ALGORITHM = "HS256"

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        print("Token received:", token, type(token))
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload  # Just return payload, not a tuple
    except jwt.PyJWTError as e:
        print("JWT Decode Error:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

def require_role(allowed_roles: list):
    def role_checker(payload=Depends(verify_token)):
        user_role = payload.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied for role: {user_role}"
            )
        return payload
    return role_checker