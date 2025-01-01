from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from schemas import SubstituteRequest, SubstituteResponse
from services.substitution_service import get_substitutions
from utils.cache import get_cache
from utils.rate_limiter import rate_limit
import uvicorn
import logging

app = FastAPI(
    title="SubstituteChef API",
    description="API for intelligent ingredient substitutions based on recipe context and dietary restrictions.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/substitute", response_model=SubstituteResponse, dependencies=[Depends(rate_limit)])
async def substitute(request: SubstituteRequest):
    try:
        cache = get_cache()
        cache_key = f"substitute:{hash(str(request))}"
        cached_response = cache.get(cache_key)
        if cached_response:
            return JSONResponse(content=cached_response)
        
        substitutions = get_substitutions(request)
        if not substitutions:
            raise HTTPException(status_code=404, detail="No suitable substitutions found.")
        
        response = {
            "status": "success",
            "substitutions": substitutions
        }
        cache.set(cache_key, response, ex=3600)  # Cache for 1 hour
        return response
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Substitution Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to SubstituteChef API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
