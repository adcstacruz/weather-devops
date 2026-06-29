import os
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException

from app.weather import fetch_weather

app = FastAPI(title="weather-devops")


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness check — no external dependencies."""
    return {"status": "ok"}


@app.get("/weather")
async def weather(city: str = "Sydney") -> dict[str, Any]:
    """Return current weather for *city*.

    Reads OPENWEATHER_API_KEY from the environment. Returns 502 if the
    upstream API is unavailable.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY", "test-key")
    try:
        return await fetch_weather(city, api_key)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Upstream weather API returned {exc.response.status_code}",
        ) from exc
