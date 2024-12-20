from pydantic import BaseModel
from typing import List

class AnalyzePRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: str
    analysis_types: List[str] = ["bug", "performance", "style", "best_practices"]