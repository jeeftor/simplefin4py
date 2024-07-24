"""Test models."""
from datetime import datetime, timezone

import pytest
from simplefin4py.model import FinancialData


def test_dates(data_200) -> None:
    try:
        fm: FinancialData = FinancialData.from_json(data_200)  # type: ignore
    except Exception as e:
        pytest.fail(f"Failed to convert JSON data to FinancialData: {e}")

    assert fm.accounts[0].balance_date.year == 2024
    assert fm.accounts[0].balance_date.month == 1
    assert fm.accounts[0].balance_date.day == 16
    assert fm.accounts[0].balance_date.hour == 7
    assert fm.accounts[0].balance_date.minute == 4
    assert fm.accounts[0].balance_date.second == 3
    assert fm.accounts[0].balance_date.tzinfo is None
    assert fm.accounts[0].last_update.tzinfo == timezone.utc



def test_financial_model(data_200) -> None:  # type: ignore
    """Test the financial model parsing."""
    try:
        fm: FinancialData = FinancialData.from_json(data_200)  # type: ignore
    except Exception as e:
        pytest.fail(f"Failed to convert JSON data to FinancialData: {e}")

    for account in fm.accounts:
        print(f"[{account.org.name} - {account.name}]")

    for org in fm.accounts_by_org_string:
        print(f":: {org}")

    for key, value in fm.accounts_by_org_object.items():  # noqa B007
        print(f":: {key}")

    assert fm.accounts[0].name == "The Bank"
    assert fm.errors[1] == "Connection to The Bank of Go may need attention"
    assert fm.x_api_message == []

    assert fm.accounts_with_errors[1].org.name == "Investments"
    assert fm.accounts[3].org.domain == "www.randombank2.com"

    for account in fm.accounts:
        print(account.inferred_account_type)
