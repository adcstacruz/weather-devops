from fastapi import FastAPI

app = FastAPI(title="weather-devops")


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness check — no external dependencies."""
    return {"status": "ok"}
