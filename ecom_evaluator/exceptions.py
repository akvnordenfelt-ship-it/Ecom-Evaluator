class AnalysisError(Exception):
    """Raised when the product evaluation cannot be completed."""


class SignupPendingConfirmation(AnalysisError):
    """Sign-up succeeded but the user must verify their email with an OTP code."""

    def __init__(self, email: str) -> None:
        super().__init__("Enter the verification code sent to your email.")
        self.email = email
