from operations.operation import Operation, OperationResult

class PingOperation(Operation):
    def __init__(self, url, count=3):
        super().__init__()
        self.url = url
        self.count = count

    def run(self):
        pass
