"""Tests for the main function."""

from datetime import datetime
from unittest import mock

from loguru import logger

from air_monitoring.data.measurement import Ecco2Measurement


example_measurement = Ecco2Measurement(
    timestamp=datetime.now(),
    reference="12345-reference",
    temperature=25.0,
    humidity=50.0,
)


@mock.patch(
    "air_monitoring.main.Ecco2.get_measurement",
    return_value=example_measurement,
)
@mock.patch(
    "air_monitoring.main.DBConnection.insert_measurement",
    side_effect=lambda measurement: logger.info(
        f"Mocking writing to DB {measurement=}"
    ),
)
def test_get_measurement(
    insert_measurement_path, get_measurement_patch
) -> None:
    """Test that the main function does not raise an AssertionError."""
    from air_monitoring.main import main

    main()
    assert True
