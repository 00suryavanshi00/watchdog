
from app.services.strategies.abstract_analysis_strategy import AnalysisStrategy
from typing import List, Dict
from app.services.ai_agent import AiAnalyzer

class CodeAnalyzer:
    """Main class for implementing multiple analyzing strats"""


    def __init__(self, agent: AiAnalyzer, strategies: List[AnalysisStrategy] = None):
        self.agent = agent
        self.strategies = strategies or []
    
    def add_strategy(self, strategy: AnalysisStrategy):
        self.strategies.append(strategy)
    
    def analyze(self, code_diff: str) -> Dict[str, dict]:
        results = {}
        for strategy in self.strategies:
            result = strategy.analyze(code_diff)
            results[result["type"]] = result["result"]
        return results