from fastapi import APIRouter, HTTPException
from ..tasks import analyze_pr
import logging
from app.models import AnalyzePRRequest, TaskStatusResponse


# TODO: add more of logging
logger = logging.getLogger("pr_analysis")

router = APIRouter()


@router.post("/analyze-pr", response_model=TaskStatusResponse)
async def analyze_pull_request(request: AnalyzePRRequest):
    try:
        task = analyze_pr.delay(
            request.repo_url,
            request.pr_number,
            request.github_token,
            request.analysis_types
        )
        logger.info(f"Task {task.id} created for PR analysis")
        return TaskStatusResponse(task_id=task.id, status="pending")
    
    except Exception as e:
        logger.error(f"Error creating analysis task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
