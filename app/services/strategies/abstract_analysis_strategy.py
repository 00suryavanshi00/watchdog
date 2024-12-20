
from app.services.ai_agent import AiAnalyzer
from abc import ABC, abstractmethod

class AnalysisStrategy(ABC):
    """Base analysis strategy class"""
    
    def __init__(self, agent: AiAnalyzer):
        self.agent = agent
        
    @abstractmethod
    def analyze(self, code_diff: str) -> dict:
        pass