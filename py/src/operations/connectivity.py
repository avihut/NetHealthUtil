from operations.speedtest import SpeedTestOp, SpeedTestOpDelegate
from operations.base_operation import Operation, OperationResult
from operations.ping import PingOp, PingOpDelegate

class ConnectivityOpDelegate(PingOpDelegate, SpeedTestOpDelegate):
    def connectivity_operation_started(self, op):
        pass

class ConnectivityResult(OperationResult):
    def __init__(self, ping_result, speedtest_result):
        super().__init__(timestamp=ping_result.timestamp)
        self.ping_result = ping_result
        self.speedtest_result = speedtest_result

    @property
    def url(self):
        return self.ping_result.url

class ConnectivityOp(Operation):
    def __init__(self, url, ping_count=3, delegate=None):
        if delegate and not isinstance(delegate, ConnectivityOpDelegate):
            raise TypeError('delegate must be of type %s' % ConnectivityOpDelegate.__name__)

        super().__init__(delegate=delegate)
        self.url = url
        self.ping_operation = PingOp(url, ping_count, delegate)
        self.speedtest_operation = SpeedTestOp(url, delegate)

    @property
    def delegate(self):
        return self._delegate

    @delegate.setter
    def delegate(self, value):
        self._delegate = value
        if hasattr(self, 'ping_operation'): self.ping_operation.delegate = value
        if hasattr(self, 'speedtest_operation'): self.speedtest_operation.delegate = value

    def run(self):
        self.delegate.connectivity_operation_started(self) if self.delegate else None
        ping_result = self.ping_operation.run()
        speedtest_result = self.speedtest_operation.run()
        return ConnectivityResult(ping_result, speedtest_result)
