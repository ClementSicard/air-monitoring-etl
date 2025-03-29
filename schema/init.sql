-- Instantiate the schema at DB startup
CREATE TABLE IF NOT EXISTS measurement (
    id SERIAL PRIMARY KEY,
    reference VARCHAR NOT NULL,
    temperature FLOAT,
    humidity FLOAT,
    measured_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_measurement UNIQUE (reference, measured_at, temperature, humidity)
);
