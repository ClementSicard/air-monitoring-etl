-- Instantiate the schema at DB startup
CREATE TABLE IF NOT EXISTS measurement (
    id SERIAL PRIMARY KEY,
    reference INT NOT NULL,
    temperature FLOAT,
    humidity FLOAT,
    measured_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
