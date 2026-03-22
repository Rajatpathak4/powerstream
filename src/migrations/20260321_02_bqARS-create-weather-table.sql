-- create weather table
-- depends: 

CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255) NOT NULL,
    temperature FLOAT NULL,
    temperature_feels FLOAT NULL,
    humidity INT  NULL,
    weather_description VARCHAR(255)  NULL,
    temp_min FLOAT  NULL,
    temp_max FLOAT NULL,
    pressure INT NULL,
    wind_speed FLOAT NULL,
    wind_direction INT NULL,
    visibility INT NULL,
    clouds INT NOT NULL,
    country VARCHAR(255)  NULL,
    sunrise_unix BIGINT  NULL,
    sunset_unix BIGINT  NULL,
    longitude FLOAT  NULL,
    latitude FLOAT  NULL,
    created_by int8 NULL,
	created_on timestamp NULL,
	updated_by int8 NULL,
	updated_on timestamp NULL,
	deleted_by int8 NULL,
	deleted_on timestamp NULL,
	updated_timestamp timestamp DEFAULT now() NULL,
	is_deleted bool DEFAULT false NOT NULL
);

CREATE INDEX idx_weather_city ON weather_data (city);
CREATE INDEX idx_weather_city_country ON weather_data (city, country);
