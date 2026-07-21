import csv
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
CLEAN_FILE = PROJECT_DIR / "data" / "clean" / "air_quality_clean.csv"

REQUIRED_COLUMNS = {
    "city",
    "country",
    "latitude",
    "longitude",
    "measured_at_utc",
    "aqi",
}


def main() -> None:
    with open(CLEAN_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    columns = set(reader.fieldnames or [])
    missing_columns = REQUIRED_COLUMNS - columns

    if missing_columns:
        raise RuntimeError(f"Missing columns: {missing_columns}")

    seen = set()

    for row in rows:
        key = (row["city"], row["measured_at_utc"])

        if key in seen:
            raise RuntimeError(f"Duplicate found: {key}")

        seen.add(key)

    sorted_rows = sorted(rows, key=lambda row: (row["measured_at_utc"], row["city"]))

    if rows != sorted_rows:
        raise RuntimeError("Clean file is not sorted chronologically")

    print("Clean file validation OK")
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    main()
