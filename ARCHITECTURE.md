# Architecture

## 1. Goal

The goal of this project is to collect air quality data automatically for several cities, store the raw API responses, rebuild a clean dataset, and load the cleaned data into a PostgreSQL data warehouse.

## 2. Global Architecture

```text
OpenWeather Air Pollution API
        ↓
GitHub Actions
        ↓
Python scripts
        ↓
data/raw/
        ↓
data/clean/air_quality_clean.csv
        ↓
PostgreSQL Data Warehouse
```

## 3. API Source

We use the OpenWeather Air Pollution API.

This API provides air quality data using city coordinates, including AQI and pollutant values such as CO, NO, NO2, O3, SO2, PM2.5, PM10, and NH3.

## 4. Orchestrator

We use GitHub Actions as the orchestrator.

It runs the pipeline automatically using a scheduled cron workflow. It also provides execution history, logs, manual runs, and secret management.

## 5. Storage

### Raw Storage

Raw data is stored in:

```text
data/raw/
```

Each raw file contains the original API response for one city and one API call.

Raw files must never be modified. They are used as the backup source of truth.

### Clean Storage

Clean data is stored in:

```text
data/clean/air_quality_clean.csv
```

This file contains all cities in one clean CSV file. It is rebuilt from the raw files and contains one row per city and per hour.

## 6. Data Warehouse

We use a PostgreSQL database hosted online with Neon.

The warehouse follows a star schema:

```text
dim_city
dim_time
fact_air_quality
```

### dim_city

Contains city information:

* city name
* country
* latitude
* longitude

### dim_time

Contains time information:

* date
* hour
* day of week
* weekend indicator

### fact_air_quality

Contains the measured values:

* AQI
* CO
* NO
* NO2
* O3
* SO2
* PM2.5
* PM10
* NH3
* city key
* time key

## 7. Justification of Choices

GitHub Actions was chosen because it is simple, free, and supports scheduled automatic execution.

OpenWeather was chosen because it provides AQI and pollutant data through a simple API.

PostgreSQL was chosen because it supports SQL queries and dimensional data warehouse modeling.

The raw and clean storage structure was chosen to respect the project requirement: raw files are immutable, and clean data can be rebuilt from raw data.
