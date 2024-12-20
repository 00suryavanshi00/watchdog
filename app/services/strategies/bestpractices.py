
from app.services.strategies.abstract_analysis_strategy import AnalysisStrategy

class BestPracticesStrategy(AnalysisStrategy):

    def analyze(self, code_diff: str) -> dict:
        prompt = f"Analyze the following code for best practices that can be followed here:\n{code_diff}"
        return {"type": "best_practices", "result": self.agent.analyze_code(prompt)}