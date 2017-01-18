from operations.connectivity import PingOpDelegate

class PingOpTerminalPresenter(PingOpDelegate):
    def new_ping_result(self, op, ping_time):
        print("Ping time to '%s': %.3f ms" % (op.hostname, ping_time), end='\r')

    def operation_finished(self, op, result):
        average_ping_time = sum(op.ping_times) / len(op.ping_times)
        print("Average ping time to '%s': %.3f ms" % (op.hostname, average_ping_time))