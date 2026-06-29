# DevOps Mastery — Curriculum

**Project:** `weather-devops` — a FastAPI weather aggregator with a Redis cache, deployed to a local Kubernetes (kind) cluster, with a full CI/CD pipeline, observability, and security scanning.

**Why this project:** the application logic is deliberately trivial (fetch weather → cache → return) so that all your effort goes into the *pipeline*, which is the thing you're here to master. The single external dependency (a weather API) is what makes it rich: it forces real lessons in secrets, resilience, and testing code that talks to the outside world.

**Test data:** the running example queries NSW cities — `Sydney` (default), plus `Newcastle`, `Wollongong`, `Wagga Wagga` as the test set. Note that weather APIs resolve *cities/points*, not whole states, so you query a city within NSW rather than "NSW" itself.

---

## Target architecture

```
                  ┌─────────────┐
 user ───────────▶│  FastAPI    │
 GET /weather     │  service    │
 ?city=Sydney     └──────┬──────┘
                         │ cache hit? ─── yes ──▶ return
                         ▼ no
                  ┌─────────────┐         ┌──────────────────┐
                  │   Redis     │◀────────│ Weather provider │──▶ OpenWeatherMap
                  │ cache-aside │  store  │ adapter (httpx)  │     (external API)
                  └─────────────┘         └──────────────────┘

  Everything above runs as containers in a local kind Kubernetes cluster,
  shipped there by a CI/CD pipeline, observed by Prometheus + Grafana.
```

## Stack

| Concern | Tool |
|---|---|
| Language / runtime | Python 3.12, FastAPI, httpx (async) |
| Dependency mgmt | uv |
| Testing | pytest, respx (HTTP mocking), coverage |
| Quality gates | ruff (lint+format), mypy (types), pre-commit |
| Container | Docker (multi-stage), docker compose |
| Cache | Redis |
| CI/CD | GitHub Actions |
| Orchestration | Kubernetes via kind (local) |
| Infra as Code | Terraform (provisions cluster + k8s resources locally) |
| Observability | Prometheus, Grafana, structured logging |
| Security | trivy, pip-audit, bandit, gitleaks |
| Deploy target | local kind cluster (cloud optional later) |

---

## How to use this with Claude Code

This curriculum is the spine. You build the pipeline **one module at a time**. Don't ask Claude to do all modules at once — that produces shallow work.

### Per-module prompt

> Read CURRICULUM.md, PROGRESS.md, and WORKFLOW.md. Tell me which module I'm on based on PROGRESS.md, then continue from the next unfinished one — that module only.

---

## Teaching model

This is how every module runs. Claude Code follows this contract.

### 1. Always start with why

Before any code, explain the *problem* the tool or pattern solves. If you don't know why something exists, you won't know when to use it or how to debug it.

### 2. Step-by-step with generated code to copy-paste

Each step:
1. **Concept** — what this is and why it matters
2. **Code** — Claude generates it; you copy-paste it into your editor and run it
3. **You run the command** — paste the output back if something's wrong
4. **Milestone check** — verify the step actually worked before moving on

You are not a passive observer. You copy-paste, you run, you read the output, you answer checkpoint questions.

### 3. Exercises

Each module has exercises you do *after* the build steps. These are hands-on interactions with the system you just built — breaking things deliberately, reading output, making small modifications. No exercises = no retention.

### 4. Milestone checks

At each milestone, Claude asks you a question or asks you to run a command and paste the result. The module does not continue until the milestone passes. This keeps you honest.

### 5. Reference answers

Each module's completed code is archived in `learning/answers/mNN_<name>/` before you redo it. Use it if you're stuck — but try first.

---

### Definition of Done

Each module below has a **DoD** checklist. A module isn't finished until every box is tickable. `PROGRESS.md` mirrors these.

---

## Module summary

| # | Module | Focus | Hrs | Tier |
|---|--------|-------|-----|------|
| 0 | Foundations | repo, uv, layout, pre-commit, health endpoint, **issue/branch/commit workflow** | 4–5 | core |
| 1 | Testing & quality gates | pytest, respx, coverage, ruff, mypy | 5–6 | core |
| 2 | CI *(skim)* | GitHub Actions, caching, matrix, branch protection, **issue auto-close + board automation** | 5–6 | core |
| 3 | Containerization | multi-stage Dockerfile, compose (app+Redis) | 6–8 | core |
| 4 | App architecture & resilience | adapter pattern, cache-aside, timeouts/retries/circuit breaker | 6–8 | core |
| 5 | Kubernetes core | kind, deployments/services, configmaps/secrets, probes | 10–12 | keystone |
| 6 | Ingress & networking | ingress controller, routing, local DNS | 4–5 | core |
| 7 | Infrastructure as Code | Terraform: cluster + k8s resources, state, modules | 6–8 | core |
| 8 | Continuous Delivery | build → registry → deploy to kind; GitOps (ArgoCD) intro | 8–10 | core |
| 9 | Observability | structured logs, Prometheus metrics, Grafana, one real alert | 8–10 | core |
| 10 | DevSecOps | trivy, pip-audit, bandit, gitleaks in the pipeline | 5–6 | core |
| 11 | Advanced deploys | rolling vs blue-green vs canary, rollback, HPA | 6–8 | core |
| 12 | Capstone | full pipeline end-to-end, runbook, README, retro | 4–6 | core |

**Total: ~77–97 hrs.** At 6 hrs/week ≈ 3.5–4 months. At 10 hrs/week ≈ 2 months.
M5 and M8–9 are the heavy, highest-value modules — budget extra patience there. You can move fast through M2 given your CI background.

---

## Module 0 — Foundations

**Objective:** establish a clean, reproducible source of truth, and the agile workflow you'll follow for every change from here on.

**Architecture focus:** project layout as a contract; dependency pinning; the pre-commit hook as your first "shift-left" quality gate; **traceability — every change traces back to a tracked work item (issue → branch → commits → PR → merge → close).**

**You build:** repo scaffold with uv, `app/` + `tests/` layout, `pyproject.toml`, ruff + mypy + pre-commit config, a FastAPI `/health` endpoint, **plus the workflow scaffolding: GitHub Issues enabled, a PR template, a Conventional-Commits convention, an issue-linked branch-naming convention, and `WORKFLOW.md` documenting it all.** (The automation that *acts* on these — auto-close, board moves — comes in Module 2 once CI exists.)

**Design decisions to weigh:** uv vs Poetry vs pip-tools; src-layout vs flat layout; what belongs in pre-commit vs CI; GitHub Issues vs an external tracker (Jira/Linear); Conventional Commits vs free-form messages; trunk-based vs GitFlow branching.

**DoD:**
- [ ] `uv run uvicorn` serves `/health` locally
- [ ] `pre-commit run --all-files` passes
- [ ] repo has a `.gitignore`, `README.md`, pinned deps
- [ ] `WORKFLOW.md` exists; PR template in `.github/`; first issue created and worked on a `feat/<n>-…` branch with a Conventional Commit referencing it

---

## Module 1 — Testing & quality gates

**Objective:** make correctness automatic and the external dependency testable.

**Architecture focus:** the test pyramid; why you mock the weather API in CI (deterministic, no rate limits, no key); coverage as signal not target.

**You build:** unit tests for the (stub) weather logic, respx-mocked tests for the HTTP adapter, coverage reporting, ruff + mypy wired as commands.

**Design decisions to weigh:** mock with recorded fixtures vs contract tests vs a sandbox; coverage threshold vs no threshold.

**Steps:**
1. Why tests? Why mock? (concept)
2. Add `app/weather.py` stub adapter → **Milestone: imports without error**
3. Wire `/weather` endpoint into `app/main.py` → **Milestone: curl returns data or 502**
4. Add `tests/test_health.py` → **Milestone: `pytest` green on health**
5. Add `tests/test_weather.py` with respx → **Milestone: all tests green, no network calls**
6. Add coverage config → **Milestone: coverage report visible**
7. Run mypy + ruff → **Milestone: both clean**

**Exercises (do these after the build steps):**
- E1: Add an unused import to `app/weather.py`, try to commit — what happens?
- E2: Remove the return type from `fetch_weather`, run `uv run mypy app/` — what does strict mode say?
- E3: Remove `@respx.mock` from one test, run pytest — what error do you get and why?
- E4: Look at the coverage report. What does the `Missing` column mean? What would cause a line to show up there?
- E5: Write one new test yourself — what happens when `city` is an empty string?

**DoD:**
- [ ] `pytest` green with the external call fully mocked
- [ ] coverage report generated
- [ ] mypy + ruff clean

---

## Module 2 — Continuous Integration *(skim)*

**Objective:** the build becomes a pure function — same input, same output, on every push — and the agile workflow becomes automated, not manual.

**Architecture focus:** runner lifecycle; dependency caching; matrix builds; branch protection as the enforcement point; **workflow automation — auto-linking and auto-closing issues from PRs (`Closes #12`), and moving project-board cards as issues/PRs change state.**

**You build:** a GitHub Actions workflow running lint + types + tests on push/PR with uv caching and branch protection; **a GitHub Projects board (Todo/In-progress/Done) with Actions that move cards automatically; and PR-merge auto-close wired up.**

**Design decisions to weigh:** single job vs parallel jobs; what gates a merge; caching strategy; **built-in GitHub Projects automation vs custom Actions; required-reviews vs solo-dev self-merge.**

**DoD:**
- [ ] CI runs and passes on a PR
- [ ] merge to main is blocked when CI fails
- [ ] merging a PR with `Closes #N` auto-closes the issue and moves its board card to Done

---

## Module 3 — Containerization

**Objective:** the artifact you test is the artifact you ship.

**Architecture focus:** multi-stage builds; layer caching; image size and surface; non-root user; compose for local multi-service (app + Redis).

**You build:** a multi-stage Dockerfile, a `.dockerignore`, and a `docker-compose.yml` running the app against a real Redis.

**Design decisions to weigh:** slim vs distroless base; build-time vs runtime deps; one image vs separate dev/prod images.

**DoD:**
- [ ] image builds and runs `/health`
- [ ] `docker compose up` brings up app + Redis together
- [ ] image runs as non-root

---

## Module 4 — App architecture & resilience

**Objective:** real behavior — actually fetch weather, cache it, and survive upstream failure.

**Architecture focus:** the adapter/port pattern (so a 2nd provider is a one-class change); Redis cache-aside with TTL; timeouts, retries with backoff, and a circuit breaker for the external call; config via env.

**You build:** the OpenWeatherMap adapter behind an interface, cache-aside in Redis, resilience wrappers, and a typed settings module.

**Design decisions to weigh:** single provider vs multi-source; cache-aside vs write-through; where the circuit breaker lives; config via env vs file vs secret store.

**Stretch:** swap in the Bureau of Meteorology (BoM) as a second provider for authentic NSW data — this is exactly the lesson the adapter pattern teaches, since it should be a one-class change.

**DoD:**
- [ ] `/weather?city=…` returns live data, cached on repeat
- [ ] upstream timeout/failure degrades gracefully (no crash)
- [ ] cache hit/miss is observable in logs

---

## Module 5 — Kubernetes core *(keystone)*

**Objective:** run the app and Redis on a real cluster you provisioned.

**Architecture focus:** the control-plane/data-plane split; Pods vs Deployments vs Services; ConfigMaps vs Secrets; liveness/readiness/startup probes; resource requests/limits; how kind maps to real k8s.

**You build:** a kind cluster, Deployment + Service for the app, a Redis Deployment + Service, ConfigMap for config, Secret for the API key, and all three probe types.

**Design decisions to weigh:** Redis in-cluster vs external; Secret vs external secret manager; probe tuning; one manifest vs kustomize overlays.

**DoD:**
- [ ] app + Redis running in kind, reachable via port-forward
- [ ] config via ConfigMap, API key via Secret (not baked into image)
- [ ] probes configured and passing

---

## Module 6 — Ingress & networking

**Objective:** reach the service by a hostname, like a real deployment.

**Architecture focus:** the ingress controller pattern; path/host routing; how cluster DNS and local `/etc/hosts` interact.

**You build:** an ingress controller in kind, an Ingress resource routing a local hostname to the service.

**Design decisions to weigh:** ingress-nginx vs alternatives; path-based vs host-based routing.

**DoD:**
- [ ] `http://weather.local` (or similar) reaches the app through ingress

---

## Module 7 — Infrastructure as Code

**Objective:** infrastructure is reproducible and reviewable, not clicked together.

**Architecture focus:** declarative vs imperative; Terraform state and why it matters; modules; using Terraform to manage the kind cluster and k8s resources locally (IaC lessons without a cloud bill).

**You build:** Terraform that provisions the kind cluster and applies the k8s resources, split into modules, with documented state handling.

**Design decisions to weigh:** Terraform vs raw manifests vs Helm; local vs remote state; what belongs in IaC vs the app repo.

**DoD:**
- [ ] `terraform apply` stands up the cluster + workloads from scratch
- [ ] `terraform destroy` cleanly tears it down

---

## Module 8 — Continuous Delivery

**Objective:** a push results in a new version running on the cluster.

**Architecture focus:** build → push to registry → deploy; image tagging strategy; pull-based GitOps vs push-based deploy; intro to ArgoCD.

**You build:** CI that builds and pushes the image to a registry, then deploys to kind; a first taste of GitOps with ArgoCD.

**Design decisions to weigh:** push deploy vs GitOps pull; tag-by-sha vs semver; promotion between environments.

**DoD:**
- [ ] merging to main ships a new image to the cluster automatically
- [ ] you can trace a commit → image tag → running pod

---

## Module 9 — Observability

**Objective:** if you can't see it, you can't operate it.

**Architecture focus:** the three pillars (logs, metrics, traces); structured logging; Prometheus scrape model; RED/USE metrics; alerting on symptoms not causes.

**You build:** structured JSON logging, Prometheus metrics (request rate, latency, cache hit-rate, upstream errors), a Grafana dashboard, and one real alert.

**Design decisions to weigh:** what to measure (RED vs USE); pull vs push metrics; alert on symptom vs cause.

**DoD:**
- [ ] dashboard shows live request + cache + upstream metrics
- [ ] one alert fires on a deliberately induced failure

---

## Module 10 — DevSecOps

**Objective:** security is a pipeline stage, not an afterthought.

**Architecture focus:** shift-left scanning; image vuln scanning; dependency auditing; static analysis; secret detection; failing the build on findings.

**You build:** trivy (image), pip-audit (deps), bandit (SAST), and gitleaks (secrets) wired into CI as gates.

**Design decisions to weigh:** fail-build vs report-only; severity thresholds; where secrets actually live.

**DoD:**
- [ ] all four scanners run in CI
- [ ] a planted vulnerability/secret is caught by the pipeline

---

## Module 11 — Advanced deploys

**Objective:** ship changes without downtime, and undo them fast.

**Architecture focus:** rolling vs blue-green vs canary tradeoffs; rollback mechanics; horizontal pod autoscaling.

**You build:** a rolling update, a blue-green or canary strategy, a tested rollback, and an HPA reacting to load.

**Design decisions to weigh:** rolling vs blue-green vs canary per risk profile; metric-driven vs manual rollback.

**DoD:**
- [ ] a bad deploy is rolled back cleanly
- [ ] HPA scales the app under simulated load

---

## Module 12 — Capstone

**Objective:** prove the whole loop and document it.

**You build:** wire everything end-to-end (commit → CI → scan → image → deploy → observe), write a runbook (how to deploy, roll back, debug), polish the README, and run a retro on what you'd do differently.

**DoD:**
- [ ] a single commit flows through the entire pipeline to a running, observable service
- [ ] runbook + README complete
- [ ] retro notes captured

---

## Stretch / deepening (after the spine)

Optional depth once the pipeline works end-to-end: multi-provider aggregation (e.g. add Bureau of Meteorology for real NSW data); distributed tracing (OpenTelemetry); Helm charts; remote Terraform state; deploying to a real free-control-plane cloud cluster; chaos testing.
