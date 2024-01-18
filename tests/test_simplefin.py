"""Tests for stuff."""

import aiohttp
import pytest
from aioresponses import aioresponses

from simplefin4py import SimpleFin
from tests.conftest import MOCK_ACCESS_URL


@pytest.mark.asyncio  # type: ignore
async def test_claim_token_good(mock_claim_token_success, mock_claim_token):
    """Test a successful claim token."""
    # Claim the token.
    access_url = await SimpleFin.claim_setup_token(mock_claim_token, proxy="localhost")
    assert access_url == MOCK_ACCESS_URL


@pytest.mark.asyncio  # type: ignore
async def test_access_402(mock_get_data_402) -> None:
    """Test a failed access token."""
    sf = SimpleFin(MOCK_ACCESS_URL)
    with pytest.raises(aiohttp.client_exceptions.ClientResponseError):
        await sf.fetch_data()


@pytest.mark.asyncio  # type: ignore
async def test_access_403(mock_get_data_403) -> None:
    """Test a failed access token."""
    sf = SimpleFin(MOCK_ACCESS_URL)
    with pytest.raises(aiohttp.client_exceptions.ClientResponseError):
        await sf.fetch_data()


@pytest.mark.asyncio  # type: ignore
async def test_access_200(mock_get_data_200: aioresponses) -> None:
    """Test a successful access token."""
    sf = SimpleFin(MOCK_ACCESS_URL, proxy="localhost")
    await sf.fetch_data()
