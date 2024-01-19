"""SimpleFIN Exceptions."""


class SimpleFinInvalidClaimTokenError(Exception):
    """Invalid claim token error."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.message = "The claim token is invalid and could not be decoded."
        super().__init__(self.message)


class SimpleFinClaimError(Exception):
    """Exception raised for errors in the claim process."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.message = "The claim token either does not exist or has already been used claimed by someone "
        "else. Receiving this could mean that the user’s transaction information has been compromised."
        super().__init__(self.message)


class SimpleFinAuthError(Exception):
    """Authentication Error (403) on Account endpoint."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.message = (
            "Authentication failed. This could be because access has been revoked or if the credentials "
            "are incorrect."
        )
        super().__init__(self.message)


class SimpleFinPaymentRequiredError(Exception):
    """A 402 error will raise a Payment Required."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.message = "Payment Required"
        super().__init__(self.message)


class SimpleFinInvalidAccountURLError(Exception):
    """Invalid authorization URL."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.message = "There was an issue parsing the Account URL."
