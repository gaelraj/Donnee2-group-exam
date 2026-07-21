import csv
import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
CLEAN_DIR = PROJECT_DIR / "data" / "clean"
CLEAN_FILE = CLEAN_DIR / "air_quality_clean.csv"

COLUMNS = [
    "city",
    "country",
    "latitude",
    "longitude",
    "measured_at_utc",
    "aqi",
    "co",
    "no_value",
    "no2",
    "o3",
    "so2",
    "pm2_5",
    "pm10",
    "nh3",
]


def unix_to_utc_hour(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime(
        "%Y-%m-%d %H:00:00"
    )


def extract_rows_from_file(filepath: Path) -> list[dict]:
    with open(filepath, "r", encoding="utf-8") as file:
        payload = json.load(file)

    city = payload["city"]
    response = payload["response"]
    rows = []

    for item in response.get("list", []):
        components = item.get("components", {})
        main = item.get("main", {})

        rows.append(
            {
                "city": city["city"],
                "country": city["country"],
                "latitude": city["latitude"],
                "longitude": city["longitude"],
                "measured_at_utc": unix_to_utc_hour(item["dt"]),
                "aqi": main.get("aqi"),
                "co": components.get("co"),
                "no_value": components.get("no"),
                "no2": components.get("no2"),
                "o3": components.get("o3"),
                "so2": components.get("so2"),
                "pm2_5": components.get("pm2_5"),
                "pm10": components.get("pm10"),
                "nh3": components.get("nh3"),
            }
        )

    return rows


def main() -> None:
    all_rows = []

    for filepath in RAW_DIR.glob("**/*.json"):
        all_rows.extend(extract_rows_from_file(filepath))

    unique_rows = {}

    for row in all_rows:
        key = (row["city"], row["measured_at_utc"])
        unique_rows[key] = row

    rows = list(unique_rows.values())
    rows.sort(key=lambda row: (row["measured_at_utc"], row["city"]))

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    with open(CLEAN_FILE, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Clean CSV rebuilt: {CLEAN_FILE}")
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    main()
