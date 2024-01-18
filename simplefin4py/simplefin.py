"""SimpleFin Class."""
from __future__ import annotations

import aiohttp
import base64

from aiohttp import BasicAuth

from .model import FinancialData
from .const import LOGGER


# import logging
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("aiohttp.client").setLevel(logging.DEBUG)


class SimpleFin:
    """SimpleFin Class."""

    # proxy: str | None

    @classmethod
    async def claim_setup_token(
        cls, setup_token: str, verify_ssl: bool = True, proxy: str | None = None
    ) -> str:
        """Exchanges a 1-time setup token for an access token."""
        claim_url = base64.b64decode(setup_token).decode("utf-8")
        auth = BasicAuth(
            login="", password=""
        )  # Replace with appropriate auth if needed

        request_params = {"ssl": verify_ssl}
        if proxy:
            request_params["proxy"] = proxy  # type:ignore

        async with cls._create_session(auth, verify_ssl) as session:
            async with session.post(claim_url, **request_params) as response:
                access_url: str = await response.text()
                return access_url

    @staticmethod
    def _create_session(
        auth: BasicAuth, verify_ssl: bool = True
    ) -> aiohttp.ClientSession:
        """Private method to create and return an aiohttp ClientSession."""
        ssl_context = False if not verify_ssl else None
        connector = aiohttp.TCPConnector(ssl=ssl_context)

        return aiohttp.ClientSession(auth=auth, connector=connector)

    def __init__(
        self, access_url: str, *, verify_ssl: bool = True, proxy: str | None = None
    ) -> None:
        """Initialize SimpleFin with an access token."""
        self.access_url = access_url
        self.verify_ssl = verify_ssl

        scheme, rest = access_url.split("//", 1)
        self.auth, rest = rest.split("@", 1)
        self.url = scheme + "//" + rest + "/accounts"
        self.username, self.password = self.auth.split(":", 1)
        self.proxy: str | None = proxy

        # self.auth already is this i think..??
        # self.auth = BasicAuth(self.username, self.password)
        # self.session = self._create_session(auth, verify_ssl)

    async def fetch_data(self) -> FinancialData:
        """Fetch financial data from SimpleFin and return as FinancialData object."""
        LOGGER.debug("Starting fetch_data in SimpleFin")

        request_params: dict[str, str | bool] = {"ssl": self.verify_ssl}
        if self.proxy:
            request_params["proxy"] = self.proxy

        # Using the existing session for the request
        async with self._create_session(self.auth, self.verify_ssl).get(
            self.access_url + "/accounts", **request_params
        ) as response:
            response.raise_for_status()
            data = await response.json()
            LOGGER.debug(f"Received data: {data}")
            financial_data: FinancialData = FinancialData.from_dict(data)  # type: ignore[attr-defined]
            LOGGER.debug(f"Parsed FinancialData: {financial_data}")
            return financial_data
