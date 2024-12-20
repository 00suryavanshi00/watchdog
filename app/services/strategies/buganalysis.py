

from app.services.strategies.abstract_analysis_strategy import AnalysisStrategy

class BugAnalysisStrategy(AnalysisStrategy):


    def analyze(self, code_diff: str) -> dict:
        prompt = f"Analyze the following code for bug or any issues:\n{code_diff}"
        return {"type": "bug_analysis", "result": self.agent.analyze_code(prompt)}