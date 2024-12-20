from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from redis import Redis
from app.config import settings
# TODO more of data inserts 
# from ..config import celery_app, redis_client
import logging, json
from app.config import redis_client, celery_app
from app.models import AnalysisResultsResponse

router = APIRouter()
logger = logging.getLogger(__name__)


def parse_redis_results(results_str: str):
    """Safely parse Redis results string to dictionary"""
    try:
        return json.loads(results_str)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing results: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error parsing analysis results"
        )


@router.get("/results/{task_id}", response_model=AnalysisResultsResponse)
async def get_task_results(task_id: str):
    """
    Get the results of a code analysis task
    
    Args:
        task_id: The ID of the Celery task
        
    Returns:
        AnalysisResultsResponse containing task status and results
        
    Raises:
        404: Task not found
        500: Error retrieving or parsing results
    """
    try:
        # Check task exists and get status
        task = AsyncResult(task_id, app=celery_app)
        if not task.ready():
            return AnalysisResultsResponse(
                task_id=task_id,
                status=task.status
            )

        # Get results from Redis
        redis_key = f"results:{task_id}"
        results = redis_client.get(redis_key)
        
        if not results:
            # Check if task completed but results not in Redis
            if task.status == "SUCCESS":
                task_result = task.get()
                # Store results in Redis for future requests
                redis_client.set(
                    redis_key,
                    json.dumps(task_result),
                    ex=3600  # expire in 1 hour
                )
                return AnalysisResultsResponse(
                    task_id=task_id,
                    status="completed",
                    results=task_result
                )
            else:
                return AnalysisResultsResponse(
                    task_id=task_id,
                    status=task.status
                )

        # Parse and return results
        parsed_results = parse_redis_results(results)
        return AnalysisResultsResponse(
            task_id=task_id,
            status="completed",
            results=parsed_results
        )

    except ConnectionError:
        logger.error("Redis connection failed")
        raise HTTPException(
            status_code=500,
            detail="Error connecting to results storage"
        )
    except Exception as e:
        logger.error(f"Error retrieving results: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving analysis results"
        )

# Optional: Add endpoint to get just the task status
@router.get("/task/{task_id}/status")
async def get_task_status(task_id: str):
    """Get just the status of a task"""
    task = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": task.status,
        "ready": task.ready()
    }