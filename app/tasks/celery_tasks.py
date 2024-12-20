from celery import Celery
from app.services.ai_agent import AiAnalyzer
from app.config import settings
import logging
from app.utils.globalmaps import STRATEGY_MAPPING
from app.models import AnalyzePRRequest
from app.services.analyzer import CodeAnalyzer
from app.services.github_integration import GitHubService
import asyncio
from typing import List
from app.config import celery_app

# celery_app = Celery("tasks")
# celery_app.conf.update(
#     broker_url=settings.CELERY_BROKER_URL,
#     result_backend=settings.CELERY_RESULT_BACKEND,
#     task_serializer="json",
#     accept_content=["json"],
#     result_serializer="json",
#     timezone=settings.TIMEZONE,
#     enable_utc=True,
# )

logger = logging.getLogger("pr_analysis")

@celery_app.task
def analyze_pr(repo_url: str, pr_number: int, github_token: str, analysis_types: List[str]) -> dict:
    try:
        github_service = GitHubService(settings.GITHUB_TOKEN)
        ai_analyzer = AiAnalyzer(
            model_name="command-r-plus",
            api_key=settings.COHERE_API_KEY
        )

        analyzer = CodeAnalyzer(ai_analyzer)
        for analysis_type in analysis_types:
            if analysis_type in STRATEGY_MAPPING:
                strategy_class = STRATEGY_MAPPING[analysis_type]
                analyzer.add_strategy(strategy_class(ai_analyzer))

        diff_details = asyncio.run(
            github_service.get_pr_diff(repo_url, pr_number)
        )

        results = {}
        for file_path, diff_info in diff_details.items():
            if diff_info["status"] != "removed":  # Skip deleted files
                diff_text = (
                    f"File: {file_path}\n"
                    f"Status: {diff_info['status']}\n"
                    f"Changes: +{diff_info['additions']}, -{diff_info['deletions']}\n\n"
                    f"Diff patch:\n{diff_info['patch']}\n\n"
                    f"Complete file content:\n{diff_info['after_content']}"
                )
                file_results = analyzer.analyze(diff_text)
                results[file_path] = file_results

        logger.info(f"Analysis completed for PR #{pr_number}")
        return {
            "status": "completed",
            "results": results
        }

    except Exception as e:
        import traceback
        logger.error(f"Error analyzing PR #{pr_number}: {str(e)}\n{traceback.format_exc()}")
        return {"status": "failed", "error": str(e)}
