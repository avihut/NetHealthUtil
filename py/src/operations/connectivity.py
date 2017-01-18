from operations.operation import Operation, OperationResult
from subprocess import Popen, PIPE
from urllib.parse import urlparse
import re

PING_CMD = 'ping'
PING_OPT_COUNT = '-c'

class PingOpResult(OperationResult):
    def __init__(self, timestamp=None, ping_times=[]):
        super().__init__(timestamp=timestamp)
        self.ping_times = ping_times

class PingOp(Operation):
    def __init__(self, url, count=3, delegate=None):
        super().__init__(delegate=delegate)
        self.url = url
        self.count = count
        parsed_url = urlparse(self.url)
        self.hostname = (parsed_url.netloc if parsed_url.netloc else parsed_url.path)

    def perform_operation(self):
        process = Popen([PING_CMD, PING_OPT_COUNT, str(self.count), self.hostname], stdout=PIPE)
        self.ping_times = []
        self.__parse_ping_cmd_output(process)
        PingOpResult(ping_times=self.ping_times)

    def __parse_ping_cmd_output(self, process):
        for ping_line in iter(process.stdout.readline, b''):
            ping_line = ping_line.decode()
            ping_time_str = self.__extract_ping_time_from_line(ping_line)
            if ping_time_str:
                self.ping_times.append(float(ping_time_str))

    def __extract_ping_time_from_line(self, line):
        matches = re.search('.*time=(\d+.\d*)', line)
        if matches:
            return m.group(1)
        return None

class SpeedTestOp(Operation):
    def __init__(self, url, delegate=None):
        super().__init__(delegate=delegate)
        self.urll = url

    def perfomr_operation(self):
        pass

class ConnectivityOp(Operation):
    def __init__(self, url, ping_count=3, delegate=None):
        super.().__init__(delegate=delegate)
        ping_op_delegate = (delegate.ping_op_delegate if hasattr(delegate, 'ping_op_delegate') else None)
        speedtest_op_delegate = (delegate.speedtest_op_delegate if hasattr(delegate, 'speedtest_op_delegate') else None)

        self.ping_operation = PingOp(url, ping_count, ping_op_delegate)
        self.speedtest_operation = SpeedTestOp(url, speedtest_op_delegate)

    def perform_operation(self):
        self.ping_operation.run()
