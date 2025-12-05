from cachetools import TTLCache
from core.redis import get_redis_client
from core.cache import get_user_cache
import redis


def get_redis() -> redis.Redis:
    return get_redis_client()


def get_local_cache() -> TTLCache:
    return get_user_cache()
