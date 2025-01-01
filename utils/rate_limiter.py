from fastapi import HTTPException, Request
from fastapi import Depends
from utils.cache import get_cache
import time

RATE_LIMIT = 100  # requests
RATE_PERIOD = 60  # seconds

def rate_limit(request: Request, cache=Depends(get_cache)):
    ip = request.client.host
    key = f"rate:{ip}"
    current = cache.get(key)
    if current and int(current) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    else:
        pipe = cache.pipeline()
        pipe.incr(key, 1)
        if not current:
            pipe.expire(key, RATE_PERIOD)
        pipe.execute()
