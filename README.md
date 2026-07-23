# Air Quality Data Pipeline

This project collects air quality data for several cities in Madagascar using the OpenWeather Air Pollution API.

The pipeline stores raw API responses, rebuilds a clean CSV file, validates the data, and loads it into a PostgreSQL data warehouse.

## Team members

- Gaël : STD24081

- Marco : STD24141

- Conelli : STD24193

- Dylan : STD24214

- Natolotra : STD24218

## Cities

- Antananarivo
- Toamasina
- Mahajanga
- Fianarantsoa
- Toliara

## Pipeline

1. Collect AQI data from OpenWeather
2. Save raw JSON files in `data/raw/`
3. Rebuild one clean CSV file in `data/clean/`
4. Validate the clean dataset
5. Load the data warehouse

## Project structure

```text
config/                 Cities configuration
data/raw/               Raw API responses, never modified
data/clean/             Clean CSV dataset
scripts/                Python pipeline scripts
sql/                    Warehouse schema
.github/workflows/      GitHub Actions orchestration
