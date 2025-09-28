from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserUpdate, UserResponse, ChangePasswordRequest
from app.controllers.v1.user import (
    get_user,
    update_profile,
    change_password,
    get_all_users
)
from app.controllers.deps import require_user, require_admin


user_router = APIRouter()

# =========================
# Ambil profile sendiri
# =========================
@user_router.get("/me", response_model=UserResponse)
async def read_me(current_user = Depends(require_user)):
    """Ambil data user sendiri"""
    return get_user(current_user)

# =========================
# Update profile sendiri
# =========================
@user_router.put("/me", response_model=UserResponse)
async def update_me(
    payload: UserUpdate,
    current_user = Depends(require_user),
    db: Session = Depends(get_db)
):
    """Update username/email (role hanya admin boleh update di controller)"""
    return update_profile(current_user, payload, db)

# =========================
# Change password
# =========================
@user_router.put("/me/password", response_model=UserResponse)
async def change_password_endpoint(
    payload: ChangePasswordRequest,
    current_user = Depends(require_user),
    db: Session = Depends(get_db)
):
    """Ganti password user"""
    user = change_password(current_user, payload.old_password, payload.new_password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect"
        )
    return user

# =========================
# Admin: Ambil semua user
# =========================
@user_router.get("/", response_model=list[UserResponse])
async def read_all_users(db: Session = Depends(get_db), current_user = Depends(require_admin)):
    """Ambil semua user, admin-only"""
    return get_all_users(db)
