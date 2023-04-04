from abc import ABC


class BusinessLogicError(Exception, ABC):
    """
    The error representing an unexpected behavior in business logic.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
