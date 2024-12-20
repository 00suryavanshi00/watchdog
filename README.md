# watchdog


code_review_agent/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── analyze.py
│   │   ├── status.py
│   │   └── results.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_agent.py
│   │   ├── analysis_strategies.py
│   │   ├── code_fetcher.py
│   │   └── result_cache.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── celery_tasks.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── redis_client.py
├── tests/
│   ├── __init__.py
│   ├── test_analyze.py
│   ├── test_status.py
│   └── test_results.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── .env.example
