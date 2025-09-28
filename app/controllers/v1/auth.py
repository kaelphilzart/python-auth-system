from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.user import User
from app.models.auth import Auth
from datetime import timedelta, datetime, timezone
from app.core.security import verify_password, hash_password, create_access_token, create_refresh_token, decode_token
from fastapi import HTTPException, status

# =========================
# Login user
# =========================
def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None

    # Buat access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role
        },
        expires_delta=access_token_expires
    )


    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=timedelta(days=7) 
    )
    auth_entry = Auth(user_id=user.id, refresh_token=refresh_token, last_login=datetime.now(timezone.utc))
    db.add(auth_entry)
    db.commit()
    db.refresh(auth_entry)

    return {"user": user, "access_token": access_token, "refresh_token": refresh_token}

# =========================
# Register user
# =========================
def register_user(db: Session, username: str, email: str, password: str):
    existing = db.query(User).filter((User.email==email) | (User.username==username)).first()
    if existing:
        return None 

    hashed = hash_password(password)
    user = User(username=username, email=email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
# =========================
# Optional: refresh token
# =========================
def refresh_access_token(db: Session, refresh_token: str):
    """Generate access token baru dari refresh token yang valid."""
    auth_entry = db.query(Auth).filter(Auth.refresh_token == refresh_token).first()
    if not auth_entry:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    user = db.query(User).filter(User.id == auth_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role
        },
        expires_delta=access_token_expires
    )

    return access_token