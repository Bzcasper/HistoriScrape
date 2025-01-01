# api/index.py
from fastapi import FastAPI
from mangum import Mangum
from fastapi.responses import JSONResponse

app = FastAPI()
handler = Mangum(app)

@app.get("/api/health")
async def health_check():
    return {"status": "operational"}

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Resource not found",
            "path": request.url.path
        }
    )