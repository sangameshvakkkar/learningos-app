# LearningOS Backend

FastAPI service for LearningOS v0.1.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

Swagger is available at `http://localhost:8000/docs`.
