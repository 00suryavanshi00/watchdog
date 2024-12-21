from pydantic import BaseModel
from typing import List, Optional

class AnalyzePRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str]
    analysis_types: List[str] = ["bug", "performance", "style", "best_practices"]