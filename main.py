from fastapi import FastAPI
# from app.routers import example
from app.routes import pr_analysis, results, github_webhook, flush_cache
app = FastAPI()

# Include routers
app.include_router(pr_analysis.router)
app.include_router(results.router)
app.include_router(github_webhook.router)
app.include_router(flush_cache.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
