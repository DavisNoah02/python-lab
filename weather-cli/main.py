import asyncio
import sys
from typing import Optional
from httpx import AsyncClient, HTTPStatusError
from pydantic import BaseModel, Field


# 1. Pydantic Model for Type Validation & Schema Enforcement
class WeatherReport(BaseModel):
    city: str
    temperature: float
    windspeed: float
    weather_code: int = Field(description="WMO Weather interpretation code")

    @property
    def condition_text(self) -> str:
        """Translates WMO weather code to readable text."""
        codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            61: "Slight rain",
            95: "Thunderstorm",
        }
        return codes.get(self.weather_code, f"Unknown code ({self.weather_code})")


# 2. Async Service Layer
class WeatherService:
    GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, client: AsyncClient):
        self.client = client

    async def get_coordinates(self, city: str) -> Optional[tuple[float, float, str]]:
        """Fetch latitude and longitude for a city name."""
        response = await self.client.get(self.GEO_URL, params={"name": city, "count": 1})
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return None

        result = data["results"][0]
        return result["latitude"], result["longitude"], result["name"]

    async def fetch_weather(self, city: str) -> Optional[WeatherReport]:
        """Orchestrates geocoding and weather fetching."""
        location = await self.get_coordinates(city)
        if not location:
            return None

        lat, lon, official_name = location
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
        }

        response = await self.client.get(self.WEATHER_URL, params=params)
        response.raise_for_status()
        current = response.json()["current_weather"]

        return WeatherReport(
            city=official_name,
            temperature=current["temperature"],
            windspeed=current["windspeed"],
            weather_code=current["weathercode"],
        )


# 3. Application Entry Point
async def main():
    city_input = sys.argv[1] if len(sys.argv) > 1 else "Nairobi"

    async with AsyncClient(timeout=10.0) as client:
        service = WeatherService(client)
        try:
            print(f"Fetching weather for '{city_input}'...")
            report = await service.fetch_weather(city_input)

            if not report:
                print(f"Error: Location '{city_input}' not found.")
                return

            print("\n--- WEATHER REPORT ---")
            print(f"City:        {report.city}")
            print(f"Temp:        {report.temperature}°C")
            print(f"Condition:   {report.condition_text}")
            print(f"Wind Speed:  {report.windspeed} km/h")
            print("----------------------")

        except HTTPStatusError as exc:
            print(f"HTTP Error occurred: {exc.response.status_code}")
        except Exception as err:
            print(f"Unexpected error: {err}")


if __name__ == "__main__":
    asyncio.run(main())
