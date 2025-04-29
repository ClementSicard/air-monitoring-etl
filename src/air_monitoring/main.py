"""Entrypoint."""

from pathlib import Path

import click
from dotenv import load_dotenv
from loguru import logger

from air_monitoring.data.ecco2 import Ecco2
from air_monitoring.db.connection import DBConnection


@click.command()
@click.option(
    "--env-file",
    help="Path to the .env file with database connection parameters.",
)
def main(env_file: Path) -> None:
    """Main entry point for the application script."""
    logger.info(f"Starting job with env_file {env_file}...")
    load_dotenv(dotenv_path=env_file, override=True)
    ecco2 = Ecco2()
    measurement = ecco2.get_measurement()
    logger.success(f"Successfully fetched {measurement=}")

    db = DBConnection(env_file_path=env_file)
    db.insert_measurement(measurement)


if __name__ == "__main__":
    main()
