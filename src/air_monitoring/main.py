"""Entrypoint."""

from loguru import logger

from air_monitoring.data.ecco2 import Ecco2
from air_monitoring.db.connection import DBConnection


def main() -> None:
    """Main entry point for the application script."""
    logger.info("Starting job...")
    ecco2 = Ecco2()
    measurement = ecco2.get_measurement()
    logger.success(f"Successfully fetched {measurement=}")

    db = DBConnection()
    db.insert_measurement(measurement)


if __name__ == "__main__":
    main()
