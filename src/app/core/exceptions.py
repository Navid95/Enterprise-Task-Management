class DomainError(Exception):
    """
    Base class for all domain exceptions
    """

    def __init__(self, *, context: dict | None = None):
        super().__init__()
        self.context = context or dict()
