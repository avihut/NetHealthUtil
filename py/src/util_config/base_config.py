from store import Store


class UtilConfig:
    def __init__(self):
        self.store = Store()

    def load(self):
        pass


class ConfigValidationError(Exception):
    def __init__(self, message='', displayed_error=True):
        super().__init__(message)
        self.displayed_error = displayed_error
