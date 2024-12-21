from fastapi import APIRouter, HTTPException
from ..tasks import analyze_pr
import logging, hashlib
from app.models import AnalyzePRRequest, TaskStatusResponse
from app.config import redis_client


# TODO: add more of logging
logger = logging.getLogger("pr_analysis")

router = APIRouter()

def gen_cache_key(request: AnalyzePRRequest):
    return hashlib.md5(f"{request.repo_url}-{request.pr_number}-{request.github_token}-{request.analysis_types}".encode()).hexdigest()

@router.post("/analyze-pr", response_model=TaskStatusResponse)
async def analyze_pull_request(request: AnalyzePRRequest):
    try:

        cache_key = gen_cache_key(request)

        # if key exists return completed directly
        cached_status = redis_client.get(f"{cache_key}_status")
        cached_task_id = redis_client.get(f"{cache_key}_task_id")

        if cached_status:
            logger.info(f"Cache hit for task {cache_key} with status {cached_status}")
            return TaskStatusResponse(task_id=cached_task_id, status=f"Cached!")


        task = analyze_pr.delay(
            request.repo_url,
            request.pr_number,
            request.github_token,
            request.analysis_types
        )

        # caching with pending status
        redis_client.set(f"{cache_key}_status", "pending")
        redis_client.set(f"{cache_key}_task_id", task.id)

        logger.info(f"Task {task.id} created for PR analysis")
        logger.info(f"Cache miss for task {task.id}")
        return TaskStatusResponse(task_id=task.id, status="pending")
    
    except Exception as e:
        logger.error(f"Error creating analysis task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
