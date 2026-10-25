# Project rules
This is an AI-assisted educational portfolio. Preserve transparent attribution.
Build one small, complete feature per run from the first unfinished TASKS.md item.
Read existing code and previous learning notes before editing. Do not duplicate features.
Use FastAPI, SQLAlchemy 2 and PostgreSQL; synchronous APIs are fine initially.
Write meaningful tests for success, invalid input, permissions and state changes.
Never weaken or remove existing tests to obtain a pass. Preserve working endpoints.
Never commit credentials, real customer data, generated binary files or database files.
Do not run git commit/push: the trusted workflow publishes after verification.
Only edit app/, tests/, migrations/, docs/learning/, TASKS.md and README.md.
Do not edit automation/, .github/, dependencies, AGENTS.md or configuration.
Use existing installed dependencies. If blocked, leave files unchanged and explain.
Do not use mock implementations or empty changes to meet a commit quota.
Mark exactly one task done only when implemented and tested.
Add an Uzbek Latin learning note under docs/learning/ for that task:
what changed, why, how to run it, design tradeoffs, 3 interview questions and answers,
and one small exercise for the repository owner. Do not claim the owner wrote the code.
When all tasks are done, stop; extending the roadmap requires an explicit new plan.

For real PostgreSQL integration tests use TEST_DATABASE_URL when supplied; never a production database. Local tests may skip PostgreSQL-only cases if this variable is absent.
