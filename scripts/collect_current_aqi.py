import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import requests


PROJECT_DIR = Path(__file__).resolve().parents[1]
CITIES_FILE = PROJECT_DIR / "config" / "cities.json"
RAW_DIR = PROJECT_DIR / "data" / "raw"


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def load_cities() -> list[dict]:
    with open(CITIES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def collect_city_air_quality(city: dict, api_key: str) -> None:
    url = "https://api.openweathermap.org/data/2.5/air_pollution"

    params = {
        "lat": city["latitude"],
        "lon": city["longitude"],
        "appid": api_key,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    collected_at = datetime.now(timezone.utc).replace(microsecond=0)

    payload = {
        "city": city,
        "collected_at_utc": collected_at.isoformat(),
        "source": "openweather_air_pollution_current",
        "response": response.json(),
    }

    city_dir = RAW_DIR / slugify(city["city"])
    city_dir.mkdir(parents=True, exist_ok=True)

    filename = collected_at.isoformat().replace(":", "-")
    filepath = city_dir / f"{filename}.json"

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    print(f"Saved raw file: {filepath}")


def main() -> None:
    api_key = os.environ.get("OPENWEATHER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY is missing")

    cities = load_cities()

    for city in cities:
        collect_city_air_quality(city, api_key)


if __name__ == "__main__":
    main()
