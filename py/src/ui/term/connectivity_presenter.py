from operations import PingOpDelegate
from ui.term.spinner import Spinner

class PingOpTerminalPresenter(PingOpDelegate):
    def new_ping_result(self, op, ping_number, total_pings_count, ping_time):
        print("\rPing %d/%d timed to '%s': %.3f ms %s " % (ping_number, total_pings_count, op.hostname, ping_time, Spinner.get_symbol_for_index(ping_number - 1)), end='')

    def operation_finished(self, op, result):
        average_ping_time = sum(op.ping_times) / len(op.ping_times)
        print("\rAverage ping time to '%s': %.3f ms               " % (op.hostname, average_ping_time))