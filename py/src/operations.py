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

    def run(self):
        pass

class DnsLookupDelegate(OperationDelegate):
    def dnslookup_started(self, op):
        pass

    def dnslookup_finished(self, op, result):
        pass

class DnsLookupResult(OperationResult):
    def __init__(self, timestamp=None, ipv4s={}, ipv6s={}):
        super().__init__(timestamp=timestamp)
        self.ipv4s = ipv4s
        self.ipv6s = ipv6s

class DnsLookupOp(Operation):
    def __init__(self, url, delegate=None):
        if delegate and not isinstance(delegate, DnsLookupDelegate):
            raise TypeError('delegate must be of type DnsLookupDelegate')

        super().__init__(delegate=delegate)
        self.url = url
        parsed_url = urlparse(self.url)
        self.hostname = (parsed_url.netloc if parsed_url.netloc else parsed_url.path)

    def run(self):
        delegate = self.delegate
        delegate.dnslookup_started(self) if delegate else None

        ip = socket.gethostbyname(self.hostname)
        result = DnsLookupResult(ipv4s = {ip})

        delegate.dnslookup_finished(self, result) if delegate else None
        return result


PING_CMD = 'ping'
PING_OPT_COUNT = '-c'

class PingOpDelegate(OperationDelegate):
    def ping_operation_started(self, op):
        pass

    def ping_operation_finished(self, op, result):
        pass

    def new_ping_result(self, op, ping_number, total_pings_count, ping_time):
        pass

class PingOpResult(OperationResult):
    def __init__(self, timestamp=None, ping_times=[]):
        super().__init__(timestamp=timestamp)
        self.ping_times = ping_times

    @property
    def average_ping_time(self):
        return sum(self.ping_times) / len(self.ping_times)

class PingOp(Operation):
    def __init__(self, url, count=3, delegate=None):
        if delegate and not isinstance(delegate, PingOpDelegate):
            raise TypeError('delegate must be of type PingOpDelegate')

        super().__init__(delegate=delegate)
        self.url = url
        self.count = count
        parsed_url = urlparse(self.url)
        self.hostname = (parsed_url.netloc if parsed_url.netloc else parsed_url.path)

    def run(self):
        delegate = self.delegate
        delegate.ping_operation_started(self) if delegate else None

        process = Popen([PING_CMD, PING_OPT_COUNT, str(self.count), self.hostname], stdout=PIPE)
        self.ping_times = []
        self.__parse_ping_cmd_output(process)
        result = PingOpResult(ping_times=self.ping_times)

        delegate.ping_operation_finished(self, result)
        return result

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

    def perform_operation(self):
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
