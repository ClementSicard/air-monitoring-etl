"""Module to setup Ecco2 sensor data source."""

from datetime import datetime
import os

from loguru import logger
from lxml import etree
import pytz
import requests

from air_monitoring.data.measurement import Ecco2Measurement

from typing import ClassVar


class Ecco2:
    """Class to get data from Ecco2 sensors."""

    # Class attributes
    dev_id: str
    token: str

    # Class constants
    BASE_URL: ClassVar[str] = "https://live.ecco2.ch/data"

    XPATH_TO_TEMP: ClassVar[str] = (
        r"/html/body/main/div[2]/div/table/tbody/tr[1]/td[2]/span[1]"
    )
    XPATH_TO_HUM: ClassVar[str] = (
        r"/html/body/main/div[2]/div/table/tbody/tr[2]/td[2]/span[1]"
    )
    XPATH_TO_REFERENCE: ClassVar[str] = r'//*[@id="cpi-ref-number"]'
    XPATH_TO_TIMESTAMP: ClassVar[str] = r"/html/body/main/div[2]/div/div[2]"

    def __init__(self) -> None:
        """Class constructor."""
        self.dev_id = os.environ["ECCO2_DEV_ID"]
        self.token = os.environ["ECCO2_TOKEN"]

        logger.info(
            f"Initializing Ecco2 with dev_id {self.dev_id} and token {self.token}"
        )

    @property
    def _params(self) -> dict:
        """Return the parameters for the request."""
        return {
            "devId": self.dev_id,
            "token": self.token,
        }

    @property
    def _headers(self) -> dict[str, str]:
        """Return the headers for the request."""
        return {"User-Agent": self._user_agent}

    @property
    def _user_agent(self) -> str:
        """Return the user agent for the request."""
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

    def _get_page(self) -> etree.ElementBase:
        response = requests.get(
            self.BASE_URL,
            params=self._params,
            headers=self._headers,
            timeout=5,
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise Exception(
                f"Error fetching data from Ecco2: {response.status_code}"
            )
        return etree.HTML(response.content, parser=etree.HTMLParser())

    def get_measurement(self) -> Ecco2Measurement:
        """Get the measurement from the Ecco2 sensor."""
        dom = self._get_page()

        temperature = dom.xpath(self.XPATH_TO_TEMP)[0].text
        humidity = dom.xpath(self.XPATH_TO_HUM)[0].text
        reference = dom.xpath(self.XPATH_TO_REFERENCE)[0].text
        raw_timestamp = dom.xpath(self.XPATH_TO_TIMESTAMP)[0].attrib.get(
            "data-last-timestamp"
        )
        return Ecco2Measurement(
            reference=reference,
            temperature=float(temperature),
            humidity=float(humidity),
            timestamp=datetime.fromtimestamp(
                int(raw_timestamp), tz=pytz.timezone("Europe/Zurich")
            ),
        )
