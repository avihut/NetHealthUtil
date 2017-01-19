from operations import PingOpDelegate, OperationDelegate
from ui.term.spinner import Spinner

class DnsLookupTerminalPresenter(OperationDelegate):
    def present_dns_lookup_op(self, op, result_pending=True):
        op_description = "DNS LOOKUP '%s': " % op.hostname
        if result_pending:
            print(op_description, end='')
        else:
            print(op_description)

    def present_dns_lookup_result(self, result):
        print("IPv4: %s, IPv6: %s" % (str(result.ipv4s), str(result.ipv6s)))

class PingOpTerminalPresenter(PingOpDelegate):
    def present_op(self, op):
        print("Measure latency to '%s' %s" % (op.hostname, Spinner.get_symbol_for_index(0)), end='')

    def present_op_with_intermediate_ping_result(self, op, ping_time, ping_number, total_pings_count, override_prev_line=True):
        print("%sPing %d/%d timed to '%s': %.3f ms %s " % (
            ('\r' if override_prev_line else ''),
            ping_number,
            total_pings_count,
            op.hostname,
            ping_time,
            Spinner.get_symbol_for_index(ping_number)),
            end='')

    def present_op_with_result(self, op, result, override_prev_line=True):
        print("%sAverage latency to '%s': %.3f ms%s" % (
            ('\r' if override_prev_line else ''),
            op.hostname,
            result.average_ping_time,
            ' ' * 10))
