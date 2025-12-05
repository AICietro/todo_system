import redis

redis_client = None


def get_redis_client():
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis(
            host="localhost", port=6379, db=0, protocol=3, decode_responses=True
        )
    return redis_client
