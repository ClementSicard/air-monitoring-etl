"""Module to interact with the database."""

import os

from dotenv import load_dotenv
from loguru import logger
import psycopg2

from air_monitoring.data.measurement import Ecco2Measurement


class DBConnection:
    """Class to handle the database connection and operations."""

    def __init__(self) -> None:
        """Constructor to initialize the database connection parameters."""
        load_dotenv()
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
    def _query(self) -> str:
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
                        self._query,
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
