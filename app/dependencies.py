from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.auth.service import decode_access_token
from app.database import get_session
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username: str | None = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
