from datetime import datetime

class Operation:
    def run(self):
        pass

class OperationResult:
    def __init__(self, timestamp=None):
        self.timestamp = (timestamp if timestamp else datetime.now())
