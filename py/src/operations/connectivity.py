from operation import Operation

class PingOperation(Operation):
    def __init__(self, url, count=3):
        self.url = url
        self.count = count

    def run(self):
        pass
