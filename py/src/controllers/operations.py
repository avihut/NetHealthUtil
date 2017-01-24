from view.term.presenters import DnsLookupTerminalPresenter, PingOpTerminalPresenter, SpeedTestOpTerminalPresenter, ConnectivityPresenter
from operations import DnsLookupDelegate, ConnectivityOpDelegate, DnsLookupResult, PingOpResult, ConnectivityResult, SpeedTestResult

class OperationsController(DnsLookupDelegate, ConnectivityOpDelegate):
    def __init__(self, operations, previous_results=[]):
        self.operations = operations
        self.previous_results = previous_results
        self.results = []
        self._initialize_presenters()

    def run(self):
        self.results = []
        for op in self.operations:
            if op:
                op.delegate = self
                result = op.run()
                self.results.append(result)
                comparable_result = self._find_last_comparable_result(result)
                if comparable_result:
                    self._show_difference_in_results(result, comparable_result)

    def _find_last_comparable_result(self, result):
        comparable_results = list(filter(lambda x: type(x) == type(result) and x.url == result.url, self.previous_results))
        comparable_results.sort()
        return comparable_results[-1]

    def _show_difference_in_results(self, new_result, previous_result):
        self._presenter_for_result_type[type(new_result)].show_difference_between_results(new_result, previous_result)

    def _initialize_presenters(self):
        self._dns_lookup_presenter = DnsLookupTerminalPresenter()
        self._ping_op_presenter = PingOpTerminalPresenter()
        self._speedtest_op_presenter = SpeedTestOpTerminalPresenter()
        self._conectivity_op_presenter = ConnectivityPresenter()

        self._presenter_for_result_type = {
            DnsLookupResult: self._dns_lookup_presenter,
            PingOpResult: self._ping_op_presenter,
            SpeedTestResult: self._speedtest_op_presenter,
            ConnectivityResult: self._conectivity_op_presenter
        }

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
