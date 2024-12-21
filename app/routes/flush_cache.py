from fastapi import APIRouter
from app.config import redis_client

router = APIRouter()

@router.get("/clear-cache")
async def clear_cache():
    redis_client.flushdb() 
    return {"status": "Cache cleared"}
