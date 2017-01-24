from datetime import datetime


class OperationResult:
    def __init__(self, timestamp=None):
        self.timestamp = (timestamp if timestamp else datetime.now())

    def __gt__(self, other):
        return self.timestamp > other.timestamp


class OperationDelegate:
    def operation_started(self, op):
        pass

    def operation_finished(self, op, result):
        pass


class Operation:
    def __init__(self, delegate=None):
        self.result = None
        self.delegate = delegate

    def run(self):
        pass
