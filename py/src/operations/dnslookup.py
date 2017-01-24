from operations.base_operation import Operation, OperationResult, OperationDelegate
from urllib.parse import urlparse
from socket import AddressFamily
import socket

class DnsLookupDelegate(OperationDelegate):
    def dnslookup_started(self, op):
        pass

    def dnslookup_finished(self, op, result):
        pass

class DnsLookupResult(OperationResult):
    def __init__(self, url, timestamp=None, ipv4s=set(), ipv6s=set()):
        super().__init__(timestamp=timestamp)
        self.url = url
        self.ipv4s = ipv4s
        self.ipv6s = ipv6s


_HTTP_PORT = 80


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

        ipv4s = set()
        ipv6s = set()
        for connection_info in socket.getaddrinfo(self.hostname, _HTTP_PORT):
            ip = connection_info[4][0]
            ip_type = connection_info[0]
            if ip_type == AddressFamily.AF_INET:
                ipv4s.add(ip)
            elif ip_type == AddressFamily.AF_INET6:
                ipv6s.add(ip)

        result = DnsLookupResult(self.url, ipv4s=ipv4s, ipv6s=ipv6s)

        delegate.dnslookup_finished(self, result) if delegate else None
        return result