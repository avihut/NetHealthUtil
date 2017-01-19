from operations.base_operation import Operation, OperationResult, OperationDelegate
from urllib.parse import urlparse
import socket

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