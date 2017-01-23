from operations.base_operation import Operation, OperationResult, OperationDelegate
from subprocess import Popen, PIPE
from urllib.parse import urlparse
import re

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
    def __init__(self, url, timestamp=None, ping_times=[]):
        super().__init__(timestamp=timestamp)
        self.url = url
        self.ping_times = ping_times

    @property
    def average_ping_time(self):
        return sum(self.ping_times) / len(self.ping_times)

class PingOp(Operation):
    def __init__(self, url, count=3, delegate=None):
        if delegate and not isinstance(delegate, PingOpDelegate):
            raise TypeError('delegate must be of type %s' % PingOpDelegate.__name__)

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
        self._parse_ping_cmd_output(process)
        result = PingOpResult(url=self.url, ping_times=self.ping_times)

        delegate.ping_operation_finished(self, result) if delegate else None
        return result

    def _parse_ping_cmd_output(self, process):
        pings_count = 1
        for ping_line in iter(process.stdout.readline, b''):
            ping_line = ping_line.decode()
            ping_time_str = self._extract_ping_time_from_line(ping_line)
            if ping_time_str:
                ping_time = float(ping_time_str)
                self.ping_times.append(ping_time)
                self.delegate.new_ping_result(self, pings_count, self.count, ping_time) if self.delegate else None
                pings_count += 1

    def _extract_ping_time_from_line(self, line):
        matches = re.search('.*time=(\d+.\d*)', line)
        if matches:
            return matches.group(1)
        return None