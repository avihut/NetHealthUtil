from operations.operation import OperationDelegate

class DnsLookupTerminalPresenter(OperationDelegate):
    def __init__(self):
        super().__init__()

    def operation_started(self, op):
        print("DNS LOOKUP '%s': " % op.hostname, end='')

    def operation_finished(self, result):
        print("IPv4: %s, IPv6: %s" % (str(result.ipv4s), str(result.ipv6s)))
