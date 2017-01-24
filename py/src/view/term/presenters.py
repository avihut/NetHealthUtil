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
        result_strings = []
        if result.ipv4s:
            result_strings.append('IPv4: %s' % result.ipv4s)
        if result.ipv6s:
            result_strings.append('IPv6: %s' % result.ipv6s)

        if result_strings:
            print('%s' % ', '.join(result_strings))
        else:
            print('No IP addresses were found for host.')

    def show_difference_between_results(self, new_result, previous_result):
        new_ipv4s = new_result.ipv4s - previous_result.ipv4s
        deprecated_ipv4s = previous_result.ipv4s - new_result.ipv4s
        new_ipv6s = new_result.ipv6s - previous_result.ipv6s
        deprecated_ipv6s = previous_result.ipv6s - new_result.ipv6s

        differences = []
        if new_ipv4s:
            differences.append('New IPv4 addresses: %s' % new_ipv4s)
        if deprecated_ipv4s:
            differences.append('Deprecated IPv4 adresses: %s' % deprecated_ipv4s)
        if new_ipv6s:
            differences.append('New IPv6 addresses: %s' % new_ipv6s)
        if deprecated_ipv6s:
            differences.append('Deprecated IPv6 addresses: %s' % deprecated_ipv6s)

        if differences:
            print("DNS changes for '%s': %s" % (new_result.url, '. '.join(differences)))


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

    @staticmethod
    def show_difference_between_results(new_result, previous_result):
        ping_difference = new_result.average_ping_time - previous_result.average_ping_time
        if ping_difference != 0:
            difference = "longer" if ping_difference > 0 else "shorter"
            print("Latency to %s is %s by %.3f ms since last time" % (new_result.hostname, difference, abs(ping_difference)))


_SPEED_MAGNITUDES = {
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

    @staticmethod
    def _formatted_speed(speed):
        magnitude = SpeedTestOpTerminalPresenter._determine_speed_magnitude(speed)
        speed /= 10**(3*magnitude)
        return (speed, _SPEED_MAGNITUDES[magnitude])

    @staticmethod
    def _determine_speed_magnitude(speed):
        digits = 0
        while speed > 0:
            speed //= 10
            digits += 1
        digits = (digits - 1 if digits > 0 else digits)
        return digits // 3

    @staticmethod
    def show_difference_between_results(new_result, previous_result):
        speed_difference = new_result.average_download_speed - previous_result.average_download_speed
        if speed_difference != 0:
            difference = "faster" if speed_difference > 0 else "slower"
            speed, magnitude = SpeedTestOpTerminalPresenter._formatted_speed(abs(speed_difference))
            print("Download speed from %s is %s by %.2f %s since last time" % (new_result.url, difference, speed, magnitude))


class ConnectivityPresenter:
    def present_op(self, op):
        print("CONNECTIVITY test to '%s':" % op.url)

    def show_difference_between_results(self, new_result, previous_result):
        PingOpTerminalPresenter.show_difference_between_results(new_result.ping_result, previous_result.ping_result)
        SpeedTestOpTerminalPresenter.show_difference_between_results(new_result.speedtest_result, previous_result.speedtest_result)
