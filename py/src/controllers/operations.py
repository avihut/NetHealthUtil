from view.term.presenters import DnsLookupTerminalPresenter, PingOpTerminalPresenter, SpeedTestOpTerminalPresenter, ConnectivityPresenter
from operations import DnsLookupDelegate, ConnectivityOpDelegate

class OperationsController(DnsLookupDelegate, ConnectivityOpDelegate):
    def __init__(self):
        self.operations = []
        self._initialize_presenters()

    def run(self):
        for op in self.operations:
            if op:
                op.delegate = self
                op.run()

    def _initialize_presenters(self):
        self._dns_lookup_presenter = DnsLookupTerminalPresenter()
        self._ping_op_presenter = PingOpTerminalPresenter()
        self._speedtest_op_presenter = SpeedTestOpTerminalPresenter()
        self._conectivity_op_presenter = ConnectivityPresenter()

    # MARK: DnsLookupDelegate

    def dnslookup_started(self, op):
        self._dns_lookup_presenter.present_dns_lookup_op(op)

    def dnslookup_finished(self, op, result):
        self._dns_lookup_presenter.present_dns_lookup_result(result)

    # MARK: PingOpDelegate

    def ping_operation_started(self, op):
        self._ping_op_presenter.present_op(op)

    def ping_operation_finished(self, op, result):
        self._ping_op_presenter.present_op_with_result(op, result)

    def new_ping_result(self, op, ping_number, total_pings_count, ping_time):
        self._ping_op_presenter.present_op_with_intermediate_ping_result(op, ping_time, ping_number, total_pings_count)

    # MARK: SpeedTestOpDelegate

    def speedtest_started(self, op):
        self._speedtest_op_presenter.present_op(op)

    def speedtest_new_speed_measurement(self, op, speed, progress):
        self._speedtest_op_presenter.present_speed_measurement_and_progress(op, speed, progress)

    def speedtest_finished(self, op, result):
        self._speedtest_op_presenter.present_op_with_result(op, result)

    def speedtest_failed(self, op, error_message):
        self._speedtest_op_presenter.present_speedtest_error(op, error_message)

    # MARK: ConnectivityOpDelegate

    def connectivity_operation_started(self, op):
        self._conectivity_op_presenter.present_op(op)
