from datetime import datetime

class OperationResult:
    def __init__(self, timestamp=None):
        self.timestamp = (timestamp if timestamp else datetime.now())

class OperationDelegate:
    def operation_started(self):
        pass

    def operation_finished(self, result):
        pass

class Operation:
    def __init__(self):
        self.result = None
        self.delegate = None

    def perform_operation(self):
        pass

    def run(self):
        self.delegate.operation_started() if self.delegate else None
        self.result = self.perform_operation()
        self.delegate.operation_finished(self.result) if self.delegate else None
        return self.result
