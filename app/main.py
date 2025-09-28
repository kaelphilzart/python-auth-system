import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.redis import init_redis
from app.routes.main import api_router 
from fastapi.responses import FileResponse
from pathlib import Path

PUBLIC_DIR = Path(__file__).parent / "public/html"

# =========================
# FastAPI instance
# =========================
app = FastAPI(
    title="MyApp API",
    version=settings.API_VERSION
)

@app.get("/")
def main():
    return FileResponse(PUBLIC_DIR / "index.html")

# =========================
# Init Redis
# =========================
init_redis()

# =========================
# CORS middleware
# =========================
origins = settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=settings.CORS_CREDENTIALS.lower() == "true",
    allow_methods=settings.CORS_METHODS.split(",") if settings.CORS_METHODS else ["*"],
    allow_headers=settings.CORS_HEADERS.split(",") if settings.CORS_HEADERS else ["*"],
)

# =========================
# Middleware contoh: logging
# =========================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response

# =========================
# Include central router
# =========================
app.include_router(api_router)

# =========================
# Run server
# =========================
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
