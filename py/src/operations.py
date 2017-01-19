from subprocess import Popen, PIPE
from urllib.parse import urlparse
from datetime import datetime
import socket
import re

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


class DnsLookupResult(OperationResult):
    def __init__(self, timestamp=None, ipv4s={}, ipv6s={}):
        super().__init__(timestamp=timestamp)
        self.ipv4s = ipv4s
        self.ipv6s = ipv6s

class DnsLookupOp(Operation):
    def __init__(self, url, delegate=None):
        super().__init__(delegate=delegate)
        self.url = url
        parsed_url = urlparse(self.url)
        self.hostname = (parsed_url.netloc if parsed_url.netloc else parsed_url.path)

    def perform_operation(self):
        ip = socket.gethostbyname(self.hostname)
        return DnsLookupResult(ipv4s = {ip})

PING_CMD = 'ping'
PING_OPT_COUNT = '-c'

class PingOpDelegate(OperationDelegate):
    def new_ping_result(self, op, ping_number, total_pings_count, ping_time):
        pass

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
        pings_count = 1
        for ping_line in iter(process.stdout.readline, b''):
            ping_line = ping_line.decode()
            ping_time_str = self.__extract_ping_time_from_line(ping_line)
            if ping_time_str:
                ping_time = float(ping_time_str)
                self.ping_times.append(ping_time)
                self.delegate.new_ping_result(self, pings_count, self.count, ping_time) if self.delegate else None
                pings_count += 1

    def __extract_ping_time_from_line(self, line):
        matches = re.search('.*time=(\d+.\d*)', line)
        if matches:
            return matches.group(1)
        return None

class SpeedTestOp(Operation):
    def __init__(self, url, delegate=None):
        super().__init__(delegate=delegate)
        self.urll = url

    def perfomr_operation(self):
        pass

class ConnectivityOp(Operation):
    def __init__(self, url, ping_count=3, delegate=None):
        super().__init__(delegate=delegate)
        ping_op_delegate = (delegate.ping_op_delegate if hasattr(delegate, 'ping_op_delegate') else None)
        speedtest_op_delegate = (delegate.speedtest_op_delegate if hasattr(delegate, 'speedtest_op_delegate') else None)

        self.ping_operation = PingOp(url, ping_count, ping_op_delegate)
        self.speedtest_operation = SpeedTestOp(url, speedtest_op_delegate)

    def perform_operation(self):
        self.ping_operation.run()
