class BaseAuthException(Exception):
    """
    Base class for all authentication & authorization exceptions.
    """

    def __init__(self, *, context: dict | None = None):
        super().__init__()
        self.context = context or dict()


class AuthenticationError(BaseAuthException):
    """
    Exception indicating lack of or unaccepted credentials
    """

    def __init__(self, reason: str | None = None):
        super().__init__(context={
            "reason": reason
        })
