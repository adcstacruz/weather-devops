# Module 1 — Testing & Quality Gates

## What this module covers

Writing a deterministic test suite for code that calls an external HTTP API, wiring coverage reporting, and making mypy (strict) and ruff clean.

---

## The test pyramid

```
        /\
       /  \   E2E  — tests the full deployed system (Module 8+)
      /----\
     / integ \  integration — tests real DB/cache connections (Module 3+)
    /----------\
   /  unit/mock  \  ← we are here
  /______________\
```

In this module we sit at the base: fast, in-process tests that mock every external dependency. The rule is simple — **tests must be able to run with no network access, no API key, no running services.**

---

## How respx works

`respx` is an httpx-native mock library. It intercepts at the httpx *transport* layer — the same layer a real network call goes through — so your production code (`fetch_weather`) doesn't know it's being mocked.

```python
@respx.mock
def test_weather_success() -> None:
    respx.get("https://api.openweathermap.org/...").mock(
        return_value=httpx.Response(200, json={...})
    )
    # any httpx.AsyncClient().get(...) to that URL returns the mock
    response = client.get("/weather?city=Sydney")
    assert response.status_code == 200
```

Why `@respx.mock` as a decorator (not a context manager)?
- It activates only for the duration of the test function.
- It automatically raises if any unexpected HTTP call slips through (no silent network calls).

Alternatives considered:
- **VCR (cassettes)**: records real responses, replays them. Fixtures go stale when the API changes and you need a real key to re-record.
- **unittest.mock.patch**: patching `httpx.AsyncClient` at the class level is fragile — breaks if the import path changes.
- **Contract tests (Pact)**: strongest correctness guarantee but heavy infrastructure for one API.

---

## What we built

### `app/weather.py` — the stub adapter

```
fetch_weather(city, api_key) → dict[str, Any]
    └── httpx.AsyncClient.get(OPENWEATHERMAP_URL, params=...)
        └── response.raise_for_status()   ← non-2xx becomes HTTPStatusError
        └── return response.json()
```

"Stub" means the *shape* is real (right URL, right params, right return type) but there is no resilience: no retry, no timeout, no circuit breaker. Those come in Module 4.

### `app/main.py` — `/weather` endpoint

Wires `fetch_weather` into FastAPI. Catches `httpx.HTTPStatusError` and re-raises as HTTP 502. Why 502 (Bad Gateway)?

- 502 = "I asked someone else and they failed" — semantically correct for a proxy/aggregator.
- 500 = "I crashed" — misleading, the app itself is fine.
- The caller can distinguish "upstream is down" (502) from "app bug" (500).

### Tests

| Test | What it proves |
|------|----------------|
| `test_health_returns_ok` | /health is dependency-free |
| `test_weather_success` | happy path, data flows through |
| `test_weather_default_city_is_sydney` | default param works |
| `test_weather_upstream_error_returns_502` | 5xx upstream → 502 |
| `test_weather_city_not_found_returns_502` | 404 upstream → 502 |
| `test_weather_nsw_cities[Newcastle/Wollongong/Wagga Wagga]` | parametrized, city name passes through |

---

## Coverage

```
Name             Stmts   Miss  Cover
------------------------------------
app/main.py         16      0   100%
app/weather.py       9      0   100%
TOTAL               25      0   100%
```

100% here is a side effect of the codebase being small, not a target. The important thing: **no untested branches**. Once the codebase grows and hitting 100% becomes hard, focus coverage analysis on the `Missing` column — those are the branches worth investigating, not the percentage.

---

## mypy strict mode

`strict = true` in `pyproject.toml` enforces:
- Every argument and return type annotated
- No implicit `Any` (explicit `Any` from `typing` is allowed)
- No calls to untyped functions

Practical implication: `dict[str, Any]` is the honest return type for JSON from an external API — we don't know its shape statically. Using `Any` explicitly is fine; *implicit* `Any` is what strict mode bans.

---

## ruff

Two distinct commands, one tool:

```bash
uv run ruff check app/ tests/   # lint (unused imports, style issues, etc.)
uv run ruff format app/ tests/  # format (replaces black)
```

pre-commit runs both automatically on every commit (`--fix` for check, format for format). Running them manually before committing gives faster feedback.

---

## Key commands

```bash
uv run pytest                         # run tests + coverage
uv run pytest -v                      # verbose (see each test name)
uv run pytest tests/test_weather.py   # run one file
uv run mypy app/ tests/               # type-check
uv run ruff check app/ tests/         # lint
uv run ruff format app/ tests/        # format
```

---

## Lessons / things worth remembering

- `@respx.mock` makes unexpected HTTP calls raise an error — this is the right default. If a test silently makes a real network call, it's not a unit test.
- Test the *behaviour* of the endpoint (status codes, response shape), not the implementation (don't assert that `fetch_weather` was called with specific args — that's brittle).
- The `OPENWEATHERMAP_URL` constant is exported from `app/weather.py` and imported in tests. This means if the URL ever changes, only one place needs updating.
- mypy strict + 100% coverage caught nothing in this module because the code is simple. In Module 4 (resilience) the types get harder and the value becomes obvious.
