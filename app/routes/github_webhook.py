from fastapi import APIRouter, Header, HTTPException, Request
from app.models import AnalyzePRRequest, TaskStatusResponse
import requests
import os
import hmac
import hashlib, logging
from ..tasks import analyze_pr
from ..config import settings

router = APIRouter()


GITHUB_WEBHOOK_SECRET = settings.GITHUB_WEBHOOK_SECRET
logger = logging.getLogger("webhook")

def verify_signature(payload: bytes, signature: str) -> bool:
    if not GITHUB_WEBHOOK_SECRET:
        raise ValueError("GITHUB_WEBHOOK_SECRET is not set.")
    computed_signature = 'sha256=' + hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature)

@router.post("/github-webhook")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None)
):
    # verify signature
    body = await request.body()
    if not verify_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=403, detail="Invalid signature")


    payload = await request.json()

    # doing only for prs
    if x_github_event == "pull_request":
        # incoming payload
        repo_url = payload["repository"]["html_url"]
        pr_number = payload["pull_request"]["number"]
        github_token = os.getenv("GITHUB_TOKEN") 
        analysis_types = ["bug_analysis"]  

        try:

            task = analyze_pr.delay(
                pr_number,
                github_token,
                repo_url,
                analysis_types
        )
            logger.info(f"Task {task.id} created for PR analysis")
            return TaskStatusResponse(task_id=task.id, status="pending")
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error triggering analysis: {str(e)}")
    else:
        return {"status": "ignored", "message": f"Unhandled event type: {x_github_event}"}
