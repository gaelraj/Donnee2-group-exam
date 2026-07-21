import csv
import os
from datetime import datetime
from pathlib import Path

import psycopg2


PROJECT_DIR = Path(__file__).resolve().parents[1]
CLEAN_FILE = PROJECT_DIR / "data" / "clean" / "air_quality_clean.csv"


def connect():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is missing")

    return psycopg2.connect(database_url)


def get_or_create_city(cursor, row: dict) -> int:
    cursor.execute(
        """
        INSERT INTO dim_city (
            city_name,
            country,
            latitude,
            longitude
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (city_name, country)
        DO UPDATE SET
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude
        RETURNING city_id;
        """,
        (
            row["city"],
            row["country"],
            float(row["latitude"]),
            float(row["longitude"]),
        ),
    )

    return cursor.fetchone()[0]


def get_or_create_time(cursor, measured_at_utc: str) -> int:
    dt = datetime.strptime(measured_at_utc, "%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO dim_time (
            measured_at_utc,
            date_value,
            hour_value,
            day_of_week,
            month_value,
            year_value,
            is_weekend
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (measured_at_utc)
        DO UPDATE SET
            date_value = EXCLUDED.date_value
        RETURNING time_id;
        """,
        (
            dt,
            dt.date(),
            dt.hour,
            dt.isoweekday(),
            dt.month,
            dt.year,
            dt.isoweekday() in [6, 7],
        ),
    )

    return cursor.fetchone()[0]


def to_float(value):
    if value in [None, ""]:
        return None

    return float(value)


def main() -> None:
    connection = connect()

    try:
        with open(CLEAN_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        with connection.cursor() as cursor:
            for row in rows:
                city_id = get_or_create_city(cursor, row)
                time_id = get_or_create_time(cursor, row["measured_at_utc"])

                cursor.execute(
                    """
                    INSERT INTO fact_air_quality (
                        city_id,
                        time_id,
                        aqi,
                        co,
                        no_value,
                        no2,
                        o3,
                        so2,
                        pm2_5,
                        pm10,
                        nh3
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (city_id, time_id)
                    DO UPDATE SET
                        aqi = EXCLUDED.aqi,
                        co = EXCLUDED.co,
                        no_value = EXCLUDED.no_value,
                        no2 = EXCLUDED.no2,
                        o3 = EXCLUDED.o3,
                        so2 = EXCLUDED.so2,
                        pm2_5 = EXCLUDED.pm2_5,
                        pm10 = EXCLUDED.pm10,
                        nh3 = EXCLUDED.nh3;
                    """,
                    (
                        city_id,
                        time_id,
                        int(row["aqi"]),
                        to_float(row["co"]),
                        to_float(row["no_value"]),
                        to_float(row["no2"]),
                        to_float(row["o3"]),
                        to_float(row["so2"]),
                        to_float(row["pm2_5"]),
                        to_float(row["pm10"]),
                        to_float(row["nh3"]),
                    ),
                )

        connection.commit()
        print(f"Warehouse loaded successfully: {len(rows)} rows")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
