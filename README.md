# fastapi-lab

Small FastAPI projects I build to learn backend fundamentals before larger SaaS work.

## Projects

| Project | What it demonstrates | Status |
|---|---|---|
| [extractor](./extractor) | File upload validation, dependency injection, structured LLM output, arithmetic cross-checks | In progress |

## Running a project

# example
    cd extractor
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env     # add your key
    pytest -q
    fastapi dev app/main.py