"""SimpleFIN Exceptions."""


class ClaimError(Exception):
    """Exception raised for errors in the claim process."""

    def __init__(self) -> None:
        """Initialize the exception."""
        self.message = "The claim token either does not exist or has already been used claimed by someone "
        "else. Receiving this could mean that the user’s transaction information has been compromised."
        super().__init__(self.message)
