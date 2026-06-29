# Module 1 — Reference Answer

This is the complete working solution for Module 1. Use it if you're stuck — but try first.

## Files

| File | What it is |
|------|-----------|
| `weather.py` → goes in `app/weather.py` | Stub weather adapter |
| `main.py` → goes in `app/main.py` | FastAPI app with /weather endpoint |
| `test_health.py` → goes in `tests/test_health.py` | Health endpoint test |
| `test_weather.py` → goes in `tests/test_weather.py` | Weather tests with respx mocks |
| `notes.md` | Design decisions and explanations |

## pyproject.toml additions (not shown in files above)

Dev deps to add:
```
respx>=0.23.1
pytest-cov>=7.1.0
```

pytest config to add:
```toml
[tool.pytest.ini_options]
addopts = "--cov=app --cov-report=term-missing"
filterwarnings = ["ignore:Using `httpx` with `starlette.testclient`"]

[tool.coverage.run]
source = ["app"]
omit = ["app/__init__.py"]
```
