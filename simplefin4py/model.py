"""Data models."""
from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class Organization:
    """Org data."""

    domain: str
    sfin_url: str = field(metadata=config(field_name="sfin-url"))
    url: str = field(default="")
    name: str = field(default="")

    def __eq__(self, other: object) -> bool:
        """Override the default Equals behavior."""
        if isinstance(other, Organization):
            return self.domain == other.domain
        return False

    def __hash__(self) -> int:
        """Override the default hash behavior (that returns the id or the object)."""
        return hash(self.domain)


@dataclass_json
@dataclass
class Transaction:
    """Transaction data."""

    id: str
    posted: int
    amount: str
    description: str


@dataclass_json
@dataclass
class Holding:
    """Holding data."""

    id: str
    created: int
    currency: str | None  # Using `|` for optional fields
    cost_basis: str = field(metadata=config(field_name="cost-basis"))
    description: str
    market_value: str = field(metadata=config(field_name="market-value"))
    purchase_price: str = field(metadata=config(field_name="purchase-price"))
    shares: str
    symbol: str


@dataclass_json
@dataclass
class Account:
    """Account data."""

    org: Organization
    id: str
    name: str
    currency: str
    balance: str
    available_balance: str = field(metadata=config(field_name="available-balance"))
    balance_date: int = field(metadata=config(field_name="balance-date"))
    transactions: list[Transaction]
    holdings: list[Holding] = field(default_factory=list)
    extra: dict | None = None  # type: ignore

    # Optional Error field added by me
    possible_error: bool = False


@dataclass_json
@dataclass
class FinancialData:
    """Financial Data."""

    errors: list[str]
    x_api_message: list[str] = field(
        default_factory=list, metadata=config(field_name="x-api-message")
    )
    _accounts: list[Account] = field(
        default_factory=list, metadata=config(field_name="accounts")
    )

    @property
    def accounts(self) -> list[Account]:
        """Getter for accounts that sets the error flag based on the error state."""
        error_account_names = [
            a.replace("Connection to ", "").replace(" may need attention", "")
            for a in self.errors
        ]

        for account in self._accounts:
            # Set error flag if the account name is in the list of error account names
            if account.org.name in error_account_names:
                account.possible_error = True
        return self._accounts

    @accounts.setter
    def accounts(self, value: list[Account]) -> None:  # pragma: no cover
        """Setter for accounts."""
        self._accounts = value

    @property
    def accounts_with_errors(self) -> list[Account]:
        """Getter for accounts with errors."""
        """Return accounts that may be in error."""
        return [x for x in self.accounts if x.possible_error]

    @property
    def accounts_by_org_string(self) -> dict[str, list[Account]]:
        """Getter for accounts by org."""
        return self._get_accounts_by_org(with_object=False)  # type:ignore

    @property
    def accounts_by_org_object(self) -> dict[Organization, list[Account]]:
        """Getter for accounts by org."""
        ret: dict[Organization, list[Account]] = self._get_accounts_by_org(  # type: ignore
            with_object=True
        )
        return ret

    def _get_accounts_by_org(
        self, with_object: bool = False
    ) -> dict[str | Organization, list[Account]]:
        """Getter for accounts by org."""
        grouped_accounts = {}  # type: ignore
        for account in self.accounts:
            org = account.org
            if with_object:
                key = org
            else:
                key = org.name if org.name else org.domain  # type:ignore

            if org not in grouped_accounts:
                grouped_accounts[key] = []
            grouped_accounts[key].append(account)
        return grouped_accounts
