"""SimpleFin Class."""
import aiohttp
import base64

from aiohttp import BasicAuth

from .model import FinancialData
from .const import LOGGER
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("aiohttp.client").setLevel(logging.DEBUG)


class SimpleFin:
    """SimpleFin Class."""

    @classmethod
    async def claim_setup_token(cls, setup_token: str, verify_ssl: bool = True) -> str:
        """Exchanges a 1-time setup token for an access token."""
        claim_url = base64.b64decode(setup_token).decode("utf-8")
        async with aiohttp.ClientSession() as session:
            async with session.post(claim_url, ssl=verify_ssl) as response:
                access_url: str = await response.text()
                return access_url

    def __init__(self, access_url: str, verify_ssl: bool = True) -> None:
        """Initialize SimpleFin with an access token."""
        self.access_url = access_url
        scheme, rest = access_url.split("//", 1)
        auth, rest = rest.split("@", 1)
        self.url = scheme + "//" + rest + "/accounts"
        self.username, self.password = auth.split(":", 1)
        self.verify_ssl = verify_ssl

    async def fetch_data(self) -> FinancialData:
        """Fetch financial data from SimpleFin and return as FinancialData object."""
        LOGGER.debug("Starting fetch_data in SimpleFin")

        """Fetch financial data from SimpleFin and return as FinancialData object."""
        LOGGER.debug("Starting fetch_data in SimpleFin")

        # Basic Authentication
        auth = BasicAuth(self.username, self.password)

        # Construct the full URL
        full_url = self.access_url + "/accounts"

        # Log the request details
        LOGGER.debug(
            f"Making a GET request to {full_url} with username: {self.username}"
        )

        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.get(
                self.access_url + "/accounts", ssl=self.verify_ssl
            ) as response:
                response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
                data = await response.json()
                LOGGER.debug(f"Received data: {data}")
                financial_data: FinancialData = FinancialData.from_dict(  # type: ignore
                    data
                )  # Parse JSON response into FinancialData object
                LOGGER.debug(f"Parsed FinancialData: {financial_data}")
                return financial_data
