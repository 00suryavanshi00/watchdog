# from abstract_analysis_strategy import AnalysisStrategy
from app.services.strategies.abstract_analysis_strategy import AnalysisStrategy

class PerformanceAnalysisStrategy(AnalysisStrategy):


    def analyze(self, code_diff: str) -> dict:
        prompt = f"Analyze the following code for style issues:\n{code_diff}"
        return {"type": "performance_analysis", "result": self.agent.analyze_code(prompt)}