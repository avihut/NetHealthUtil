from view.term.spinner import Spinner
import sys

class DnsLookupTerminalPresenter:
    def present_dns_lookup_op(self, op, result_pending=True):
        op_description = "DNS LOOKUP '%s': " % op.hostname
        if result_pending:
            print(op_description, end='')
        else:
            print(op_description)

    def present_dns_lookup_result(self, result):
        print("IPv4: %s, IPv6: %s" % (str(result.ipv4s), str(result.ipv6s)))

class PingOpTerminalPresenter:
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

SPEED_MAGNITUDES = {
    0: "bps",
    1: 'Kbps',
    2: 'Mbps',
    3: 'Gbps'
}

class SpeedTestOpTerminalPresenter:
    def present_op(self, op):
        print("Measuring download speed from '%s'..." % op.url, end='')
        sys.stdout.flush()

    def present_speed_measurement_and_progress(self, op, speed, progress, bar_length=20):
        speed, magnitude = self._formatted_speed(speed)
        done = int(bar_length * progress)
        remaining = int(bar_length - done)
        print("\rMeasuring download speed from '%s': [%s%s] %.2f %s" % (
            op.url,
            '=' * done,
            ' ' * remaining,
            speed,
            magnitude), end='')

    def present_op_with_result(self, op, result):
        speed, magnitude = self._formatted_speed(result.average_download_speed)
        print("\rAverage download speed from '%s': %.2f %s" % (op.url, speed, magnitude))

    def present_speedtest_error(self, op, error_message):
        print("\rFailed measuring download speed to '%s': %s" % (op.url, error_message))

    def _formatted_speed(self, speed):
        magnitude = self._determine_speed_magnitude(speed)
        speed /= 10**(3*magnitude)
        return (speed, SPEED_MAGNITUDES[magnitude])

    def _determine_speed_magnitude(self, speed):
        digits = 0
        while speed > 0:
            speed //= 10
            digits += 1
        return digits // 3

class ConnectivityPresenter:
    def present_op(self, op):
        print("CONNECTIVITY test to '%s':" % op.url)
