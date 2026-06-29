# Progress Tracker

**How to use:** Claude Code updates this as you complete each module's Definition of Done. `[ ]` = todo, `[x]` = done. Add dated notes under each module as you learn things worth remembering.

**Status legend:** ⬜ not started · 🟡 in progress · ✅ done

---

## Overview

| # | Module | Status | Hrs (est) | Hrs (actual) |
|---|--------|--------|-----------|--------------|
| 0 | Foundations | ✅ | 4–5 | 1 |
| 1 | Testing & quality gates | ⬜ | 5–6 | |
| 2 | CI (skim) | ⬜ | 5–6 | |
| 3 | Containerization | ⬜ | 6–8 | |
| 4 | App architecture & resilience | ⬜ | 6–8 | |
| 5 | Kubernetes core | ⬜ | 10–12 | |
| 6 | Ingress & networking | ⬜ | 4–5 | |
| 7 | Infrastructure as Code | ⬜ | 6–8 | |
| 8 | Continuous Delivery | ⬜ | 8–10 | |
| 9 | Observability | ⬜ | 8–10 | |
| 10 | DevSecOps | ⬜ | 5–6 | |
| 11 | Advanced deploys | ⬜ | 6–8 | |
| 12 | Capstone | ⬜ | 4–6 | |

**Total target:** ~77–97 hrs.

---

## Module 0 — Foundations
- [x] `uv run uvicorn` serves `/health`
- [x] `pre-commit run --all-files` passes
- [x] `.gitignore`, `README.md`, pinned deps present
- [x] `WORKFLOW.md` + PR template present; first issue worked on a `feat/<n>-…` branch with a Conventional Commit referencing it

_Notes: 2026-06-29 — scaffold complete. uv 0.9.18, fastapi 0.138.1, ruff 0.15.20, mypy 2.1.0.
pre-commit hooks: trailing-whitespace, end-of-file-fixer, check-yaml, check-toml, ruff lint, ruff-format.
Issue #1 → branch feat/1-m0-foundations → this PR. Conventional Commits enforced from first commit._

## Module 1 — Testing & quality gates
- [ ] `pytest` green with external call mocked
- [ ] coverage report generated
- [ ] mypy + ruff clean

_Notes:_

## Module 2 — CI (skim)
- [ ] CI runs and passes on a PR
- [ ] merge to main blocked when CI fails
- [ ] merging a PR with `Closes #N` auto-closes the issue and moves its board card to Done

_Notes:_

## Module 3 — Containerization
- [ ] image builds and runs `/health`
- [ ] `docker compose up` brings up app + Redis
- [ ] image runs as non-root

_Notes:_

## Module 4 — App architecture & resilience
- [ ] `/weather?city=…` returns live data, cached on repeat
- [ ] upstream failure degrades gracefully
- [ ] cache hit/miss visible in logs

_Notes:_

## Module 5 — Kubernetes core
- [ ] app + Redis running in kind (port-forward reachable)
- [ ] config via ConfigMap, API key via Secret
- [ ] probes configured and passing

_Notes:_

## Module 6 — Ingress & networking
- [ ] local hostname reaches the app through ingress

_Notes:_

## Module 7 — Infrastructure as Code
- [ ] `terraform apply` builds cluster + workloads from scratch
- [ ] `terraform destroy` tears down cleanly

_Notes:_

## Module 8 — Continuous Delivery
- [ ] merge to main ships a new image automatically
- [ ] commit → image tag → running pod is traceable

_Notes:_

## Module 9 — Observability
- [ ] dashboard shows live request + cache + upstream metrics
- [ ] one alert fires on an induced failure

_Notes:_

## Module 10 — DevSecOps
- [ ] all four scanners run in CI
- [ ] a planted vuln/secret is caught

_Notes:_

## Module 11 — Advanced deploys
- [ ] a bad deploy is rolled back cleanly
- [ ] HPA scales under simulated load

_Notes:_

## Module 12 — Capstone
- [ ] one commit flows through the entire pipeline to a running service
- [ ] runbook + README complete
- [ ] retro notes captured

_Notes:_
