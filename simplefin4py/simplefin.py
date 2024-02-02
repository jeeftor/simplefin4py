"""SimpleFin Class."""
from __future__ import annotations

import binascii

import aiohttp
import base64

from aiohttp import BasicAuth, ClientConnectorError, ClientConnectorSSLError

from .exceptions import (
    SimpleFinClaimError,
    SimpleFinInvalidClaimTokenError,
    SimpleFinInvalidAccountURLError,
    SimpleFinPaymentRequiredError,
    SimpleFinAuthError,
)
from .model import FinancialData
from .const import LOGGER


# import logging
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("aiohttp.client").setLevel(logging.DEBUG)


class SimpleFin:
    """SimpleFin Class."""

    @classmethod
    def decode_claim_token(cls, token_string: str) -> str:
        """Decode a claim token string - or throws an error."""
        try:
            claim_url = base64.b64decode(token_string).decode("utf-8")
        except binascii.Error as err:
            raise SimpleFinInvalidClaimTokenError from err
        return claim_url

    @classmethod
    def decode_access_url(cls, access_url: str) -> tuple[str, str, str]:
        """Decode an access URL string - or throws an error."""
        try:
            scheme, rest = access_url.split("//", 1)
            auth, rest = rest.split("@", 1)
        except ValueError as err:
            raise SimpleFinInvalidAccountURLError from err

        return scheme, rest, auth

    @classmethod
    async def claim_setup_token(
        cls, setup_token: str, verify_ssl: bool = True, proxy: str | None = None
    ) -> str:
        """Exchanges a 1-time setup token for an access token."""
        claim_url = cls.decode_claim_token(setup_token)

        auth = BasicAuth(
            login="", password=""
        )  # Replace with appropriate auth if needed

        request_params = {"ssl": verify_ssl}
        if proxy:
            request_params["proxy"] = proxy  # type:ignore

        ssl_context = False if not verify_ssl else None
        connector = aiohttp.TCPConnector(ssl=ssl_context)

        async with aiohttp.ClientSession(auth=auth, connector=connector) as session:
            response = await session.post(claim_url, **request_params)
            if response.status == 403:
                # Claim issue
                raise SimpleFinClaimError()
            access_url: str = await response.text()
            return access_url

    def __init__(
        self, access_url: str, *, verify_ssl: bool = True, proxy: str | None = None
    ) -> None:
        """Initialize SimpleFin with an access token."""
        self.access_url = access_url
        self.verify_ssl = verify_ssl

        scheme, rest, self.auth = self.decode_access_url(access_url)
        # try:
        #     scheme, rest = access_url.split("//", 1)
        #     self.auth, rest = rest.split("@", 1)
        # except ValueError as err:
        #     raise SimpleFinInvalidAccountURLError from err
        self.url = scheme + "//" + rest + "/accounts"
        self.username, self.password = self.auth.split(":", 1)
        self.proxy: str | None = proxy

    async def fetch_data(self) -> FinancialData:
        """Fetch financial data from SimpleFin and return as FinancialData object.

        This method attempts to retrieve financial data from a given SimpleFin endpoint.
        It raises specific exceptions for HTTP status codes 402 and 403, indicating
        payment required and authentication errors, respectively. Additionally, it
        captures and re-raises `ClientConnectorError` and `ClientConnectorSSLError`
        for lower-level connection issues.

        Raises:
            SimpleFinPaymentRequiredError: Raised when the response status is 402 (Payment Required).
            SimpleFinAuthError: Raised when the response status is 403 (Forbidden).
            ClientConnectorError: Raised for general connection errors.
            ClientConnectorSSLError: Raised for SSL-related connection errors.        return self.coordinator.data.get_account_for_id(self.account_id).currency

            Exception: General exception for any other errors that might occur.

        Returns:
            FinancialData: The financial data retrieved from SimpleFin.
        """
        LOGGER.debug("Starting fetch_data in SimpleFin")

        request_params: dict[str, str | bool] = {"ssl": self.verify_ssl}
        if self.proxy:
            request_params["proxy"] = self.proxy

        ssl_context = False if not self.verify_ssl else None
        connector = aiohttp.TCPConnector(ssl=ssl_context)

        try:
            async with aiohttp.ClientSession(
                auth=self.auth, connector=connector
            ) as session:
                response = await session.get(
                    self.access_url + "/accounts", **request_params
                )

                if response.status == 402:
                    raise SimpleFinPaymentRequiredError()
                if response.status == 403:
                    raise SimpleFinAuthError()

                data = await response.json()
                LOGGER.debug(f"Received data: {data}")
                financial_data: FinancialData = FinancialData.from_dict(data)  # type: ignore[attr-defined]
                LOGGER.debug(f"Parsed FinancialData: {financial_data}")
                return financial_data
        except (ClientConnectorError, ClientConnectorSSLError) as err:
            raise err
        except Exception as e:
            print(e)
            raise e
