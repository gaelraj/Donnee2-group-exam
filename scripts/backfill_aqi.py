import argparse
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


def date_to_unix(date_string: str) -> int:
    date_value = datetime.strptime(date_string, "%Y-%m-%d")
    date_value = date_value.replace(tzinfo=timezone.utc)
    return int(date_value.timestamp())


def backfill_city(city: dict, api_key: str, start_date: str, end_date: str) -> None:
    url = "https://api.openweathermap.org/data/2.5/air_pollution/history"

    params = {
        "lat": city["latitude"],
        "lon": city["longitude"],
        "start": date_to_unix(start_date),
        "end": date_to_unix(end_date),
        "appid": api_key,
    }

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()

    payload = {
        "city": city,
        "backfill_start_date": start_date,
        "backfill_end_date": end_date,
        "source": "openweather_air_pollution_history",
        "response": response.json(),
    }

    city_dir = RAW_DIR / slugify(city["city"])
    city_dir.mkdir(parents=True, exist_ok=True)

    filepath = city_dir / f"backfill_{start_date}_to_{end_date}.json"

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    print(f"Backfill saved: {filepath}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)

    args = parser.parse_args()

    api_key = os.environ.get("OPENWEATHER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY is missing")

    cities = load_cities()

    for city in cities:
        backfill_city(
            city=city,
            api_key=api_key,
            start_date=args.start,
            end_date=args.end,
        )


if __name__ == "__main__":
    main()
