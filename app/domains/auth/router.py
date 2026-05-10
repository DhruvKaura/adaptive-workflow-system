from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import get_db
from app.core.security.dependencies import get_current_user
from app.core.security.rate_limit import limiter
from app.domains.auth.models import User
from app.domains.auth.schemas import Token, UserCreate
from app.domains.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


# -----------------------------------
# Register User
# -----------------------------------


@router.post("/register")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):

    user = await AuthService.register_user(db, user_data)

    return {"message": "User registered successfully", "user_id": str(user.id)}


# -----------------------------------
# Login User
# -----------------------------------


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):

    token = await AuthService.authenticate_user(
        db, form_data.username, form_data.password
    )

    if not token:

        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": token, "token_type": "bearer"}


# -----------------------------------
# Current User
# -----------------------------------


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):

    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "username": current_user.username,
    }
