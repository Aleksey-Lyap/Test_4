class ExpectedError(Exception):
    def __init__(self, reason: str) -> None:
        self.name = self.__class__.__name__
        self.reason = reason
        super().__init__(f'{self.name}: {self.reason}')


class WrongFormatError(ExpectedError):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason
