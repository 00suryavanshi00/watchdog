# WatchDog

## Overview

WatchDog is an autonomous code review agent system using AI to analyze GitHub pull requests. It processes code reviews asynchronously with Celery, interacting with developers through a structured FastAPI-based API.

## Access the deployed version here 👇
```bash
http://35.244.62.43/docs
```

### Prerequisites

1. **Python 3.8+**
2. **Redis** (or PostgreSQL for task/result storage)
3. **Celery** for asynchronous task processing
4. **FastAPI** for building the API
5. **Any LLM API** (e.g., OpenAI, Ollama for local model running I've used cohere)

### Project setup instructions

Clone the repository:

```bash
git clone git@github.com:00suryavanshi00/watchdog.git
cd watchdog
sudo apt install docker (your system equivalent of this)
docker compose up --build (for v2 docker compose )/ docker-compose up --build(for v1 docker compose)
```

This should spin up redis and app instance you should be able to see the {"message": "Welcome to FastAPI!"} on visiting
``` localhost:8000```

### Api Documentation
Post the application starts visit 
```bash
locahost:8000/docs
--> NOTE: leave github_token as empty string to pick up the default token (mine in the deployed version) in analyze_pr api
```
to access local doc api playground for yourself and for the deployed one it's mentioned above.

### Design Decisions

1. **Separation of Concerns**:
    - Organized into folders: `routers`, `services`, `tasks`, and `utils`.
    - Each layer has a specific responsibility (e.g., routing, task handling, AI services).
2.  **Scalability**:
    - AI-based `CodeAnalyzer` uses the **Strategy Pattern**, making it easy to add new analysis strategies.
3. **Logging**:
    - Centralized logging with clear messages for task tracking.
5. **Celery for Asynchronous Processing**:
    - Scales task execution and avoids blocking the main thread.
6. **Redis for Task Results**:
    - Efficient and scalable storage for analysis results.
7. **Environment Variables**:
    - Sensitive data like tokens and credentials are securely loaded using `os.getenv`.
8. **Ai Model**:
    - Cohere is being used because I'm out of openai credits :) 
9. **Webhook Support**:
    - WatchDog also has a webhook api for only pr events which is tested and can be directly added to the repo with the link and secret. Here's an example use case with my personal repo.
    
    ![Car Image](https://storage.googleapis.com/ecoroots_assets_bucket/github/WhatsApp%20Image%202024-12-21%20at%2016.07.36.jpeg)
10. **Rate Limiting**:
    - WatchDog is also ratelimited by nginx on number of requests per second from a specific IP address. Below is the snippet from nginx config.
    
    ```bash
    http {
    limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;

    server {
        listen 80;

        # Apply rate limiting to all requests
        location / {
            limit_req zone=mylimit burst=5 nodelay;
            
            # rest configs
            try_files $uri $uri/ =404;
        }
    }
}
    ```
11. ***Caching***:
    - WatchDog also caches the requests if everything in the payload is exactly same. It doesn't create a new celery task id for it.


