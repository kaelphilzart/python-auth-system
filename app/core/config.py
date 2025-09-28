import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ENV = os.getenv("ENV", "LOCAL")
    PORT = int(os.getenv("PORT", 8000))
    SSL = os.getenv("SSL", "FALSE") == "TRUE"
    API_VERSION = os.getenv("API_VERSION", "1.0")
    #database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    #redis
    REDIS_URL: str = os.getenv("REDIS_URL")

    #cors
    CORS_ORIGINS = os.getenv("CORS_ORIGINS")
    CORS_CREDENTIALS = os.getenv("CORS_CREDENTIALS")
    CORS_METHODS = os.getenv("CORS_METHODS")
    CORS_HEADERS = os.getenv("CORS_HEADERS")

    #secret key
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")

settings = Settings()

