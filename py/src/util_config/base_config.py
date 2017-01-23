from store import Store


class UtilConfig:
    def __init__(self):
        self.store = Store()

    def load(self):
        pass


class ConfigError(BaseException):
    def __init__(self, message='', displayed_error=True):
        super().__init__()
        self.message = message
        self.displayed_error = displayed_error
