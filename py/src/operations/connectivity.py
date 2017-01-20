from operations.base_operation import Operation, OperationResult, OperationDelegate
from operations.ping import PingOp

class ConnectivityOp(Operation):
    def __init__(self, url, ping_count=3, delegate=None):
        super().__init__(delegate=delegate)
        ping_op_delegate = (delegate.ping_op_delegate if hasattr(delegate, 'ping_op_delegate') else None)
        speedtest_op_delegate = (delegate.speedtest_op_delegate if hasattr(delegate, 'speedtest_op_delegate') else None)

        self.ping_operation = PingOp(url, ping_count, ping_op_delegate)
        self.speedtest_operation = SpeedTestOp(url, speedtest_op_delegate)

    def perform_operation(self):
        self.ping_operation.run()
