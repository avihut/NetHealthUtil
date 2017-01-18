from operations.operation import Operation, OperationResult
from urllib.parse import urlparse
import socket

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
