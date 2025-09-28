# app/api/deps.py
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token
from app.models.user import User


def require_token(request: Request) -> str:
    """Ambil token JWT dari cookie. Raise error kalau tidak ada."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing",
        )
    return token


def require_user(
    db: Session = Depends(get_db),
    token: str = Depends(require_token),
) -> User:
    """Pastikan user login & valid di database."""
    payload = decode_token(token)
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
        )
    return user


def require_admin(current_user: User = Depends(require_user)) -> User:
    """Pastikan user punya role admin."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user
