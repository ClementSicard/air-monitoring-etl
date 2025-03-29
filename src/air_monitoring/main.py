"""Entrypoint."""

from loguru import logger

from air_monitoring.data.ecco2 import Ecco2


def main() -> None:
    """Main entry point for the application script."""
    logger.info("Starting job...")
    ecco2 = Ecco2()
    measurement = ecco2.get_measurement()
    logger.success(f"{measurement=}")


if __name__ == "__main__":
    main()
