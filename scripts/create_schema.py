import os
from pathlib import Path

import psycopg2


PROJECT_DIR = Path(__file__).resolve().parents[1]
SCHEMA_FILE = PROJECT_DIR / "sql" / "schema.sql"


def main():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is missing")

    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
        schema_sql = file.read()

    connection = psycopg2.connect(database_url)

    try:
        with connection.cursor() as cursor:
            cursor.execute(schema_sql)

        connection.commit()
        print("Warehouse schema created successfully")

    finally:
        connection.close()


if __name__ == "__main__":
    main()