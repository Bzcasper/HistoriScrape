# rate_limiter.py
from cachetools import TTLCache
from fastapi import Request, HTTPException

class RateLimiter:
    def __init__(self):
        self.cache = TTLCache(maxsize=1000, ttl=60)
    
    async def __call__(self, request: Request):
        client_ip = request.client.host
        if client_ip in self.cache:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        self.cache[client_ip] = 1
        return True

rate_limit = RateLimiter()