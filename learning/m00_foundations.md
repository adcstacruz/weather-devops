# Module 0 — Foundations

## What this module covers

Establishing a clean, reproducible project scaffold and the agile workflow (issue → branch → commit → PR → merge) that every later module follows.

---

## Design decisions

### uv (chosen) vs Poetry vs pip-tools

- **uv**: single Rust-based tool — manages the venv, resolves/installs deps, runs scripts, and produces a hermetic `uv.lock`. Fastest resolver available. Made by Astral (same team as ruff), so the two tools integrate naturally.
- **Poetry**: mature and popular, but slower resolver and heavier. Losing ground to uv.
- **pip-tools**: minimal — just compiles `requirements.txt`. No venv management. Good for simple scripts, not a full project.

**Takeaway:** for a new project started today, uv is the right call.

### Flat `app/` layout vs src-layout (`src/weather_devops/`)

- **src-layout** forces you to `pip install -e .` before any import works. This surfaces import errors that flat layouts hide — important for published libraries.
- **Flat `app/`** is simpler: the Python path includes the repo root, so `import app` just works. Appropriate for an *application* (not a library).

We use `app/` as the curriculum specifies. If this became a published package, src-layout would be the right move.

### pre-commit vs CI for quality gates

| Gate | Where | Why |
|------|--------|-----|
| ruff lint + format | pre-commit | Fast (<1s), catches trivial errors before push, runs locally |
| mypy (type-checking) | CI (Module 2) | Slower, authoritative — can't be skipped |
| Tests + coverage | CI (Module 2) | Full suite too slow for a hook |

pre-commit is a shift-left tool — it moves the feedback loop earlier. But it's *not* a replacement for CI because it can be bypassed (`--no-verify`).

### GitHub Issues vs Jira/Linear

GitHub Issues: zero extra overhead, native integration with commits (`refs #N`) and PRs (`Closes #N`), free. Jira/Linear add features (sprints, roadmaps) that aren't justified for a solo learning project.

### Conventional Commits vs free-form

Conventional Commits format: `<type>(<scope>): <summary>\n\nrefs #N`

Benefits:
- Machine-readable → auto-changelogs (e.g. `git-cliff`, `semantic-release`)
- Consistent → `git log --oneline` is actually useful
- Required input for Module 2 automation

### Trunk-based vs GitFlow

- **Trunk-based** (chosen): short-lived feature branches, merge to `main` often, simple. Right for solo dev and fast feedback.
- **GitFlow**: `develop`/`release`/`hotfix` branches. Overhead only justified for large teams shipping fixed releases.

---

## What we built

```
weather-devops/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI app with /health endpoint
├── tests/
│   └── __init__.py
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md
├── learning/
│   └── m00_foundations.md   (this file)
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml           # uv project: deps + tool config
├── README.md
├── WORKFLOW.md
├── CURRICULUM.md
└── PROGRESS.md
```

### Key files explained

**`pyproject.toml`** — single source of truth for:
- project metadata and dependencies (`[project]`)
- uv-specific config (`[tool.uv]`)
- ruff config (`[tool.ruff]`)
- mypy config (`[tool.mypy]`)

**`.pre-commit-config.yaml`** — hooks that run on every `git commit`:
- `ruff` lint (with auto-fix)
- `ruff-format` (formatter, replaces black)
- standard hooks: trailing whitespace, end-of-file newline, YAML/TOML validation

**`app/main.py`** — minimal FastAPI app. The `/health` endpoint is the first integration point for every downstream module (CI health checks, k8s probes, uptime monitoring).

---

## Key commands

```bash
# Run the app locally
uv run uvicorn app.main:app --reload

# Check the health endpoint
curl http://localhost:8000/health

# Run all pre-commit hooks against all files
uv run pre-commit run --all-files

# Add a dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>
```

---

## Lessons / things worth remembering

- `uv.lock` goes in git — it's how you get reproducible builds. `.python-version` goes in git too (pins the interpreter).
- ruff replaces both flake8 and black. One tool, one config section in `pyproject.toml`.
- The `/health` endpoint should be dependency-free (no DB, no cache) so k8s liveness probes never cascade-fail.
- `WORKFLOW.md` is the social contract for this repo: every PR must reference an issue, every issue must be small enough to finish in one PR.
