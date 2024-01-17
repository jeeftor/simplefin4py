"""This is conftest.py file."""
import json
from typing import Any

import pytest


@pytest.fixture  # type: ignore
def good_data_json() -> dict[str, Any]:
    """Good Data."""
    with open("fixtures/200-with-errors.json") as json_file:
        data = json.load(json_file)
    return data  # type: ignore[no-any-return]


@pytest.fixture  # type: ignore
def account_set_json() -> dict[str, Any]:
    """Good Data."""
    with open("fixtures/account_set.json") as json_file:
        data = json.load(json_file)
    return data  # type: ignore[no-any-return]
