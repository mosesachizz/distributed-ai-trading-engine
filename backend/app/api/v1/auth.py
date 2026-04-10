from fastapi import APIRouter, HTTPException

from app.core.security import create_access_token, get_password_hash, verify_password
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

_FAKE_ADMIN = {
    "username": "admin",
    "hashed_password": get_password_hash("admin123"),
}


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    if payload.username != _FAKE_ADMIN["username"]:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(payload.password, _FAKE_ADMIN["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(subject=payload.username)
    return TokenResponse(access_token=token)
