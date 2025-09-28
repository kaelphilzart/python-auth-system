import redis
from redis.client import Redis
from app.core.config import Settings as settings

redis_client: Redis | None = None

def init_redis(db_index: int = 0) -> None:
    """Initialize Redis connection using URL """
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            db=db_index
        )
        redis_client.ping()
        print("Redis connected")
    except Exception as e:
        print(f"Redis connection failed: {e}")
        raise e

def get_redis() -> Redis:
    """Get Redis client instance."""
    if redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return redis_client
