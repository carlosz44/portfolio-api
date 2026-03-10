from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.service import create_access_token, verify_password
from app.database import get_session
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, session: Session = Depends(get_session)):
    statement = select(User).where(User.username == body.username)
    user = session.exec(statement).first()

    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=token)
