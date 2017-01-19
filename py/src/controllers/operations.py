from ui.term.presenters import DnsLookupTerminalPresenter, PingOpTerminalPresenter
from operations import DnsLookupDelegate, PingOpDelegate

class OperationsController(DnsLookupDelegate, PingOpDelegate):
    def __init__(self):
        self.operations = []
        self.__initialize_presenters()

    def run(self):
        for op in self.operations:
            op.delegate = self
            op.run()

    def __initialize_presenters(self):
        self.__dns_lookup_presenter = DnsLookupTerminalPresenter()
        self.__ping_op_presenter = PingOpTerminalPresenter()

    # MARK: DnsLookupDelegate

    def dnslookup_started(self, op):
        self.__dns_lookup_presenter.present_dns_lookup_op(op)

    def dnslookup_finished(self, op, result):
        self.__dns_lookup_presenter.present_dns_lookup_result(result)

    # MARK: PingOpDelegate

    def ping_operation_started(self, op):
        self.__ping_op_presenter.present_op(op)

    def ping_operation_finished(self, op, result):
        self.__ping_op_presenter.present_op_with_result(op, result)

    def new_ping_result(self, op, ping_number, total_pings_count, ping_time):
        self.__ping_op_presenter.present_op_with_intermediate_ping_result(op, ping_time, ping_number, total_pings_count)