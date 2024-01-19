"""This is conftest.py file."""
import json
import os
from typing import Any
import pytest
from aioresponses import aioresponses

import base64
from collections.abc import Generator

current_dir = os.path.dirname(__file__)

MOCK_CLAIM_TOKEN = "https://claim.url"  # noqa: S105
MOCK_ACCESS_URL = "https://user:passwords@access_url"


@pytest.fixture  # type: ignore
def data_200() -> str:
    """Good Data."""
    with open(f"{current_dir}/fixtures/200-with-errors.json") as json_file:
        data = json.load(json_file)
    return json.dumps(data)


@pytest.fixture  # type: ignore
def data_402() -> str:
    """Not Paid."""
    with open(f"{current_dir}/fixtures/402.json") as json_file:
        data = json.load(json_file)
    return json.dumps(data)


@pytest.fixture  # type: ignore
def data_403() -> str:
    """Bad URL."""
    with open(f"{current_dir}/fixtures/403.txt") as text_file:
        data = "\n".join(text_file.readlines())
    return data


@pytest.fixture  # type: ignore
def account_set_json() -> dict[str, Any]:
    """Good Data."""
    with open(f"{current_dir}/fixtures/account_set.json") as json_file:
        data = json.load(json_file)
    return data  # type: ignore[no-any-return]


@pytest.fixture  # type: ignore
def mock_claim_token_success() -> Generator[aioresponses, None, None]:
    """Fixture for mocking a login process with bad credentials."""
    # Using 'aioresponses' to mock asynchronous HTTP responses.
    with aioresponses() as m:
        # Mock a failed login attempt due to bad credentials.
        m.post(MOCK_CLAIM_TOKEN, status=200, body=MOCK_ACCESS_URL)
        yield m


@pytest.fixture  # type: ignore
def mock_claim_token_403() -> Generator[aioresponses, None, None]:
    """Fixture for mocking a login process with bad credentials."""
    # Using 'aioresponses' to mock asynchronous HTTP responses.
    with aioresponses() as m:
        # Mock a failed login attempt due to bad credentials.
        m.post(MOCK_CLAIM_TOKEN, status=403, body="")
        yield m


@pytest.fixture  # type: ignore
def mock_claim_token() -> str:
    """Fixture for the claim URL."""
    return base64.b64encode(MOCK_CLAIM_TOKEN.encode("utf-8")).decode("utf-8")


@pytest.fixture()  # type: ignore
def mock_get_data_200(data_200: str) -> Generator[aioresponses, None, None]:
    """Fixture for mocking a successful fetch process."""
    with aioresponses() as m:
        # Mock a failed login attempt due to bad credentials.
        m.get(MOCK_ACCESS_URL + "/accounts", status=200, body=data_200)
        yield m


@pytest.fixture()  # type: ignore
def mock_get_data_402(data_402: str) -> Generator[aioresponses, None, None]:
    """Fixture for mocking a response for account that hasn't paid."""
    with aioresponses() as m:
        # Mock a failed login attempt due to bad credentials.
        m.get(MOCK_ACCESS_URL + "/accounts", status=402, body=data_402)
        yield m


@pytest.fixture()  # type: ignore
def mock_get_data_403(data_403: str) -> Generator[aioresponses, None, None]:
    """Fixture for mocking a fech process with bad credentials/url."""
    with aioresponses() as m:
        # Mock a failed login attempt due to bad credentials.
        m.get(MOCK_ACCESS_URL + "/accounts", status=403, body=data_403)
        yield m


@pytest.fixture()  # type: ignore
def mock_get_data_generic_error() -> Generator[aioresponses, None, None]:
    """Fixture for mocking a fech process with bad credentials/url."""
    with aioresponses() as m:
        # Mock a failed login attempt due to bad credentials.
        m.get(MOCK_ACCESS_URL + "/accounts", status=200, body="<,asduB*J(_8asdji>")
        yield m
