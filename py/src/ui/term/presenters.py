from operations import PingOpDelegate, OperationDelegate
from ui.term.spinner import Spinner

class DnsLookupTerminalPresenter(OperationDelegate):
    def operation_started(self, op):
        print("DNS LOOKUP '%s': " % op.hostname, end='')

    def operation_finished(self, op, result):
        print("IPv4: %s, IPv6: %s" % (str(result.ipv4s), str(result.ipv6s)))

class PingOpTerminalPresenter(PingOpDelegate):
    def new_ping_result(self, op, ping_number, total_pings_count, ping_time):
        print("\rPing %d/%d timed to '%s': %.3f ms %s " % (ping_number, total_pings_count, op.hostname, ping_time, Spinner.get_symbol_for_index(ping_number - 1)), end='')

    def operation_finished(self, op, result):
        average_ping_time = sum(op.ping_times) / len(op.ping_times)
        print("\rAverage ping time to '%s': %.3f ms               " % (op.hostname, average_ping_time))