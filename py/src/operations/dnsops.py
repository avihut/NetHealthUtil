from operations.operation import Operation, OperationResult
import socket

class DnsLookupResult(OperationResult):
    def __init__(self, timestamp=None, ipv4s={}, ipv6s={}):
        super().__init__(timestamp=timestamp)
        self.ipv4s = ipv4s
        self.ipv6s = ipv6s

class DnsLookup(Operation):
    def __init__(self, url, delegate=None):
        super().__init__(delegate=delegate)
        self.url = url

    def perform_operation(self):
        ip = socket.gethostbyname(self.url)
        return DnsLookupResult(ipv4s = {ip})
