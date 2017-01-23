from operations import DnsLookupOp, DnsLookupResult, ConnectivityOp, PingOpResult, SpeedTestResult, ConnectivityResult
from store import OperationsStore, ResultsStore
from json import JSONEncoder
import json


class OperationsStoreFileJSON(OperationsStore):
    def __init__(self, path):
        with open(path) as _:
            pass

        self.path = path
        self.instantiate = {
            'DnsLookup': self._create_dns_lookup_operation,
            'Connectivity': self._create_connectivity_operation
        }
        self.operations = None

    def get_operations(self):
        if not self.operations:
            self.operations = []
            with open(self.path) as operations_file:
                operations_data = json.load(operations_file)
                for operation_config in operations_data:
                    operation_name = list(operation_config.keys())[0]
                    args = operation_config[operation_name]
                    self.operations.append(self.instantiate[operation_name](args))
        return self.operations

    def reload_from_file(self):
        self.operations = None

    # In both creation functions I have cut a corner and assumed that
    # the order of arguments is identical between the JSON object and
    # the arguments order of the python object constructed.
    # A better implementation would have been an actual mapping between
    # the JSON object properties and the python objet's keword-arguments.

    @classmethod
    def _create_dns_lookup_operation(cls, args):
        args = list(args.values())
        return DnsLookupOp(*args)

    @classmethod
    def _create_connectivity_operation(cls, args):
        args = list(args.values())
        return ConnectivityOp(*args)


class ResultsStoreFileJSON(ResultsStore):
    def __init__(self, path):
        self.path = path
        self.results = None

    def get_results(self):
        if not self.results:
            self.results = []
            try:
                with open(self.path, 'r') as results_file:
                    pass
            except FileNotFoundError:
                pass
        return self.results

    def write(self, results):
        if not results:
            return

        with open(self.path, 'w+') as results_file:
            json.dump(results, results_file, cls=ResultsEncoder)

    def reload_results(self):
        self.results = None


class ResultsEncoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.encoder = {
            DnsLookupResult: self.encode_dns_lookup_result,
            PingOpResult: self.encode_ping_result,
            SpeedTestResult: self.encode_speedtest_result,
            ConnectivityResult: self.encode_connectivity_result
        }

    def default(self, o):
        try:
            encoder = self.encoder[type(o)]
        except KeyError:
            raise ValueError("Tried encoding unrecognized type: %s" % type(o))

        return encoder(o)

    def encode_dns_lookup_result(self, result):
        d = {'DNSLookupResult': dict()}
        d['DNSLookupResult']['Time'] = str(result.timestamp)
        d['DNSLookupResult']['URL'] = result.url
        d['DNSLookupResult']['IPv4'] = list(result.ipv4s)
        d['DNSLookupResult']['IPv6'] = list(result.ipv6s)
        return d

    def encode_ping_result(self, result):
        d = {'PingResult': dict()}
        d['PingResult']['Time'] = str(result.timestamp)
        d['PingResult']['URL'] = result.url
        d['PingResult']['Times'] = result.ping_times
        return d

    def encode_speedtest_result(self, result):
        d = {'SpeedTestResult': dict()}
        d['SpeedTestResult']['Time'] = result.timestamp
        d['SpeedTestResult']['URL'] = result.url
        d['SpeedTestResult']['AvgSpeedBps'] = result.average_download_speed
        return d

    def encode_connectivity_result(self, result):
        d = {'ConnectivityResult': dict()}
        d['ConnectivityResult']['Time'] = str(result.ping_result.timestamp)
        d['ConnectivityResult']['URL'] = result.ping_result.url
        d['ConnectivityResult']['PingTimes'] = result.ping_result.ping_times
        d['ConnectivityResult']['AvgSpeedBps'] = result.speedtest_result.average_download_speed
        return d
