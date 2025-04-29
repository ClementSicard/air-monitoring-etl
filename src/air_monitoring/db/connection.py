"""Module to interact with the database."""

import os
from pathlib import Path

from loguru import logger
import psycopg2

from air_monitoring.data.measurement import Ecco2Measurement


class DBConnection:
    """Class to handle the database connection and operations."""

    def __init__(self, env_file_path: Path) -> None:
        """Constructor to initialize the database connection parameters."""
        self.env_file_path = env_file_path

        self.db_name = os.environ["PG_DATABASE"]
        self.user = os.environ["PG_USER"]
        self.host = os.environ["PG_HOST"]
        self.port = os.environ["PG_PORT"]

    @property
    def params(self) -> dict[str, str]:
        """Returns the DB parameters."""
        return {
            "dbname": self.db_name,
            "user": self.user,
            "host": self.host,
            "port": self.port,
        }

    @property
    def insert_query(self) -> str:
        """Returns the SQL query to insert a measurement."""
        return """
    INSERT INTO measurement (reference, temperature, humidity, measured_at)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (reference, measured_at, temperature, humidity) DO NOTHING;
    """

    def insert_measurement(self, measurement: Ecco2Measurement) -> None:
        """Inserts a record into the measurement table."""
        try:
            with psycopg2.connect(**self.params) as conn:  # type: ignore
                with conn.cursor() as cur:
                    cur.execute(
                        self.insert_query,
                        (
                            measurement.reference,
                            measurement.temperature,
                            measurement.humidity,
                            measurement.timestamp.isoformat(),
                        ),
                    )
                    logger.success(
                        f"Inserted record {measurement} into the database successfully."
                    )
        except psycopg2.Error as e:
            logger.error(f"Database error: {e}")

    @property
    def select_query(self) -> str:
        """Returns the SQL query to select all measurements."""
        return """
    SELECT reference, temperature, humidity, measured_at
    FROM measurement
    ORDER BY measured_at DESC;
    """

    def get_measurements(self) -> list[Ecco2Measurement]:
        """Fetches all measurements from the database."""
        try:
            with psycopg2.connect(**self.params) as conn:  # type: ignore
                with conn.cursor() as cur:
                    cur.execute(self.select_query)
                    rows = cur.fetchall()
                    measurements = [
                        Ecco2Measurement(
                            reference=row[0],
                            temperature=row[1],
                            humidity=row[2],
                            timestamp=row[3],
                        )
                        for row in rows
                    ]
                    logger.success(
                        f"Fetched {len(measurements)} records from the database."
                    )
                    return measurements
        except psycopg2.Error as e:
            logger.error(f"Database error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return []
