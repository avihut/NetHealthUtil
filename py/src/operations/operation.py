from datetime import datetime

class OperationResult:
    def __init__(self, timestamp=None):
        self.timestamp = (timestamp if timestamp else datetime.now())

class OperationDelegate:
    def operation_started(self, op):
        pass

    def operation_finished(self, op, result):
        pass

class Operation:
    def __init__(self, delegate=None):
        self.result = None
        self.delegate = delegate

    def perform_operation(self):
        pass

    def run(self):
        self.delegate.operation_started(op=self) if self.delegate else None
        self.result = self.perform_operation()
        self.delegate.operation_finished(self, self.result) if self.delegate else None
        return self.result
