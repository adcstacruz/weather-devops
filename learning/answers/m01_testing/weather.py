"""Stub weather adapter — calls OpenWeatherMap via httpx.

This is the thin I/O layer only. Resilience (retries, circuit breaker,
caching) is added in Module 4.
"""

from typing import Any

import httpx

OPENWEATHERMAP_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_weather(city: str, api_key: str) -> dict[str, Any]:
    """Fetch current weather for *city* from OpenWeatherMap.

    Raises:
        httpx.HTTPStatusError: on a non-2xx response from the upstream API.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            OPENWEATHERMAP_URL,
            params={"q": city, "appid": api_key, "units": "metric"},
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return data
