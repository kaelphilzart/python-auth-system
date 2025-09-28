from fastapi import APIRouter
from app.routes.v1 import auth, user  
from app.core.config import settings

api_router = APIRouter(prefix=f"/api/v{settings.API_VERSION}")

api_router.include_router(auth.auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user.user_router, prefix="/users", tags=["Users"])
