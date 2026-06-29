# weather-devops

A FastAPI weather aggregator built as a CI/CD learning project. The app logic is deliberately trivial — fetch weather data, cache it in Redis, return it — so all effort goes into the *pipeline*.

See [`CURRICULUM.md`](CURRICULUM.md) for the full 13-module plan and [`PROGRESS.md`](PROGRESS.md) for current status.

## Stack

| Concern | Tool |
|---|---|
| Language | Python 3.12, FastAPI, httpx |
| Dependency mgmt | uv |
| Testing | pytest, respx, coverage |
| Quality gates | ruff, mypy, pre-commit |
| Container | Docker, docker compose |
| Cache | Redis |
| CI/CD | GitHub Actions |
| Orchestration | Kubernetes (kind) |
| IaC | Terraform |
| Observability | Prometheus, Grafana |
| Security | trivy, pip-audit, bandit, gitleaks |

## Local setup

```bash
# Install dependencies
uv sync

# Run the app
uv run uvicorn app.main:app --reload

# Check health
curl http://localhost:8000/health
```

## Quality gates

```bash
# Run pre-commit on all files
uv run pre-commit run --all-files

# Type-check
uv run mypy app/

# Lint
uv run ruff check app/

# Tests (Module 1+)
uv run pytest
```

## Workflow

Every change follows the loop in [`WORKFLOW.md`](WORKFLOW.md):
`issue → branch → commits (refs #N) → PR (Closes #N) → merge → auto-close`
