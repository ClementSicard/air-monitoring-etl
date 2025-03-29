"""Tests for the main function."""

from datetime import datetime
from unittest import mock

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
def test_get_measurement(get_measurement_patch) -> None:
    """Test that the main function does not raise an AssertionError."""
    from air_monitoring.main import main

    main()
    assert True
