"""Module for defining the Ecco2Measurement model."""

import pydantic as pyd

from typing import Annotated


class Ecco2Measurement(pyd.BaseModel):
    """Represents a measurement from the Ecco2 sensor."""

    timestamp: pyd.PastDatetime
    reference: str
    temperature: Annotated[float, pyd.confloat(ge=-40, le=40)]
    humidity: Annotated[float, pyd.confloat(ge=0, le=100)]
