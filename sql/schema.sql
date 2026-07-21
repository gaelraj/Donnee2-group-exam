CREATE TABLE IF NOT EXISTS dim_city (
                                        city_id SERIAL PRIMARY KEY,
                                        city_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    UNIQUE(city_name, country)
    );

CREATE TABLE IF NOT EXISTS dim_time (
                                        time_id SERIAL PRIMARY KEY,
                                        measured_at_utc TIMESTAMP NOT NULL UNIQUE,
                                        date_value DATE NOT NULL,
                                        hour_value INTEGER NOT NULL,
                                        day_of_week INTEGER NOT NULL,
                                        month_value INTEGER NOT NULL,
                                        year_value INTEGER NOT NULL,
                                        is_weekend BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_air_quality (
                                                fact_id SERIAL PRIMARY KEY,
                                                city_id INTEGER NOT NULL REFERENCES dim_city(city_id),
    time_id INTEGER NOT NULL REFERENCES dim_time(time_id),

    aqi INTEGER NOT NULL,
    co DOUBLE PRECISION,
    no_value DOUBLE PRECISION,
    no2 DOUBLE PRECISION,
    o3 DOUBLE PRECISION,
    so2 DOUBLE PRECISION,
    pm2_5 DOUBLE PRECISION,
    pm10 DOUBLE PRECISION,
    nh3 DOUBLE PRECISION,

    UNIQUE(city_id, time_id)
    );