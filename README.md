# Warehouse Order API

AI-assisted educational portfolio: FastAPI backend for inventory and orders.
Built incrementally using OpenAI Codex. The owner studies and reviews changes.

## Current implementation
- GET /health
- OpenAPI documentation at /docs
- Automated tests and an ordered roadmap
- Scheduled, tested feature increments with Uzbek learning notes
- Configuration management (Pydantic Settings) and SQLAlchemy 2 session setup
- Isolated SQLite test database support for rapid local integration testing

Authentication, inventory and orders are planned, not yet implemented.

## Local development
```sh
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
python -m pytest -q
```
PostgreSQL (when the database tasks land): `docker compose up -d db`.
Copy .env.example to .env and configure real secrets locally, never in git.

## Automation
See SETUP_UZ.md. A deterministic date-based plan selects 5–10 distinct slots
between 08:00 and 22:00 Asia/Tashkent. A lightweight scheduled gate checks every
20 minutes. Each due run implements one roadmap item, tests it, then pushes one
commit directly to main. Unfinished slots may catch up one at a time later that
day. There is no guarantee of 5–10 successful pushes: failures, budget, GitHub
schedule delays, concurrent manual edits or exhausted roadmap can reduce it.
Manual runs count toward the same daily limit. No timestamps are forged.

The AI job has read-only repository credentials; only the publication job has
write access, and it does not execute the generated application. API key is
passed only to the Codex Action. The workflow rejects changes outside allowed
source/test/learning files. Tests reduce risk but do not prove generated code safe.

Commits are attributed to warehouse-ai[bot], not impersonated as manual work.
Push count is not the same as a personal GitHub contribution count.

Pause: disable Daily AI development under Actions, or set repository variable
AI_ENABLED=false. The roadmap has 35 tasks and stops when finished; extend it
explicitly after reviewing progress. It is not an indefinite feature generator.
Dependencies use bounded ranges for this initial bootstrap; lock resolved versions
before relying on it for production. This is not a production-ready system.
