from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, RefreshRequest
from app.controllers.v1.auth import login_user, register_user, refresh_access_token
from fastapi import Body
from app.controllers.deps import require_user
from app.models.auth import Auth

auth_router = APIRouter()
# =========================
# Login
# =========================
@auth_router.post("/login")
async def login(user: LoginRequest, response: Response, db: Session = Depends(get_db)):
    result = login_user(db, user.email, user.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        max_age=1800
    )

    return {"message": "Login successful"}

# =========================
# Register
# =========================
@auth_router.post("/register",status_code=200)
async def register(user: RegisterRequest, db: Session = Depends(get_db)):
    result = register_user(db, user.username, user.email, user.password)
    if not result:
        raise HTTPException(status_code=400, detail="Email or username already exists")

    return {"message": "User registered successfully"}

# =========================
# Logout
# =========================
@auth_router.post("/logout")
def logout(response: Response, current_user=Depends(require_user), db: Session = Depends(get_db)):
    db.query(Auth).filter(Auth.user_id == current_user.id).delete(synchronize_session=False)
    db.commit()
    response.delete_cookie("access_token")

    return {"msg": "Logged out successfully"}

# =========================
# Refresh token
# =========================
@auth_router.post("/refresh-token")
def refresh_token(
    request: RefreshRequest,     
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk generate access token baru dari refresh token.
    """
    refresh_token = request.refresh_token 
    new_access_token = refresh_access_token(db, refresh_token)

    
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        max_age=1800  
    )

    return {"message": "Access token refreshed successfully"}