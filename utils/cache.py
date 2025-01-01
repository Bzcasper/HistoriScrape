import redis
import os
from functools import lru_cache

@lru_cache()
def get_cache():
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    cache = redis.Redis(host=redis_host, port=redis_port, db=0)
    return cache
