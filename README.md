# python-lab

Small Python and FastAPI projects I build to learn backend fundamentals before
starting larger SaaS products. Each project is self-contained, with its own
dependencies and tests.

## Projects

| Project | What it explores | Status |
|---|---|---|
| [extractor](./extractor) | Invoice extraction API: file upload validation, dependency injection, swappable extractor interface, arithmetic cross-checks on extracted totals | Skeleton working with a fake extractor; LLM extractor in progress |
| [fastapi-agency-api](./fastapi-agency-api) | TODO: one line, e.g. "lead capture API with routers and Pydantic schemas" | TODO |
| [weather-cli](./weather-cli) | TODO: one line on what it does | TODO |

## Running a project

Each project has its own virtual environment:

    cd extractor
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    pytest -q
    fastapi dev app/main.py

Then open http://127.0.0.1:8000/docs for the interactive API docs.

## Notes

- Projects with external API keys include a `.env.example`. Copy it to `.env`
  and fill in your own key. `.env` is never committed.
- These are learning projects, not production code. Expect rough edges.