from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.user import User
from app.schemas.user import UserUpdate
from app.core.security import hash_password, verify_password

# =========================
# Logic untuk ambil user sendiri
# =========================
def get_user(user: User) -> User:
    """Return user object apa adanya, pure logic."""
    return user

# =========================
# Logic untuk update profile
# =========================
def update_profile(user: User, payload: UserUpdate, db: Session) -> User:
    """
    Update user profile berdasarkan payload.
    Payload bisa UserUpdate (username/email/etc.)
    """
    if getattr(payload, "username", None):
        user.username = payload.username
    if getattr(payload, "email", None):
        user.email = payload.email
    if getattr(payload, "role", None):
        user.role = payload.role  

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# =========================
# Logic untuk change password
# =========================
def change_password(user: User, old_password: str, new_password: str, db: Session):
    """Ganti password user dengan validasi old_password."""
    if not verify_password(old_password, user.password):
        return None

    user.password = hash_password(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# =========================
# get all users
# =========================
def get_all_users(db: Session):
    """Return semua user, admin-only logic."""
    return db.query(User).all()
