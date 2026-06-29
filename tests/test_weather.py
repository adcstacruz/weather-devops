"""Tests for the /weather endpoint.

respx intercepts the httpx.AsyncClient call inside fetch_weather() so
no real network traffic is made. The tests are fully deterministic.
"""

import httpx
import pytest
import respx
from starlette.testclient import TestClient

from app.main import app
from app.weather import OPENWEATHERMAP_URL

client = TestClient(app)

SYDNEY_FIXTURE: dict[str, object] = {
    "name": "Sydney",
    "main": {"temp": 18.5, "humidity": 72},
    "weather": [{"description": "light rain"}],
}


@respx.mock
def test_weather_success() -> None:
    """Happy path: upstream returns 200, endpoint forwards the data."""
    respx.get(OPENWEATHERMAP_URL).mock(
        return_value=httpx.Response(200, json=SYDNEY_FIXTURE)
    )

    response = client.get("/weather?city=Sydney")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sydney"
    assert data["main"]["temp"] == 18.5


@respx.mock
def test_weather_default_city_is_sydney() -> None:
    """Omitting ?city= defaults to Sydney."""
    respx.get(OPENWEATHERMAP_URL).mock(
        return_value=httpx.Response(200, json=SYDNEY_FIXTURE)
    )

    response = client.get("/weather")

    assert response.status_code == 200


@respx.mock
def test_weather_upstream_error_returns_502() -> None:
    """When OpenWeatherMap returns a non-2xx, the endpoint returns 502."""
    respx.get(OPENWEATHERMAP_URL).mock(
        return_value=httpx.Response(503, json={"message": "service unavailable"})
    )

    response = client.get("/weather?city=Sydney")

    assert response.status_code == 502
    assert "503" in response.json()["detail"]


@respx.mock
def test_weather_city_not_found_returns_502() -> None:
    """A 404 from OpenWeatherMap (unknown city) propagates as 502."""
    respx.get(OPENWEATHERMAP_URL).mock(
        return_value=httpx.Response(404, json={"message": "city not found"})
    )

    response = client.get("/weather?city=Narnia")

    assert response.status_code == 502


@respx.mock
@pytest.mark.parametrize("city", ["Newcastle", "Wollongong", "Wagga Wagga"])
def test_weather_nsw_cities(city: str) -> None:
    """Spot-check the NSW test set passes the city name through."""
    fixture = {**SYDNEY_FIXTURE, "name": city}
    respx.get(OPENWEATHERMAP_URL).mock(return_value=httpx.Response(200, json=fixture))

    response = client.get(f"/weather?city={city}")

    assert response.status_code == 200
    assert response.json()["name"] == city
