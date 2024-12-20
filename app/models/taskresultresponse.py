from pydantic import BaseModel
from typing import Optional, Dict, Any

class AnalysisResultsResponse(BaseModel):
    task_id: str
    status: str
    results: Optional[Dict[str, Any]] = None