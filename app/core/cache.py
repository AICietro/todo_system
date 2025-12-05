from cachetools import TTLCache


user_cache = TTLCache(maxsize=1024, ttl=30)

def get_user_cache():
    return user_cache