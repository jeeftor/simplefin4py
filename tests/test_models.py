"""Test models."""
import pytest
from simplefin4py.model import FinancialData


def test_financial_model(good_data_json) -> None:  # type: ignore
    """Test the financial model parsing."""
    try:
        fm: FinancialData = FinancialData.from_dict(good_data_json)  # type: ignore
    except Exception as e:
        pytest.fail(f"Failed to convert JSON data to FinancialData: {e}")

    for account in fm.accounts:
        print(f"[{account.org.name} - {account.name}]")
