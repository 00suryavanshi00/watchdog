from app.services.strategies import BestPracticesStrategy, BugAnalysisStrategy, StyleAnalysisStrategy, PerformanceAnalysisStrategy

STRATEGY_MAPPING = {
    "bug": BugAnalysisStrategy,
    "performance": PerformanceAnalysisStrategy,
    "style": StyleAnalysisStrategy,
    "best_practices": BestPracticesStrategy
}