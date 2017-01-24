from operations import DnsLookupOp, DnsLookupResult, ConnectivityOp, PingOpResult, SpeedTestResult, ConnectivityResult
from store import OperationsStore, ResultsStore
from json import JSONEncoder
import dateutil.parser
import json


class OperationsStoreFileJSON(OperationsStore):
    def __init__(self, path):
        with open(path) as _:
            pass

        self.path = path
        self.instantiate = {
            'DNSLookup': self._create_dns_lookup_operation,
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
                    operation_data = operation_config[operation_name]
                    self.operations.append(self.instantiate[operation_name](operation_data))
        return self.operations

    def reload_from_file(self):
        self.operations = None

    @classmethod
    def _create_dns_lookup_operation(cls, data):
        url = data['URL']
        return DnsLookupOp(url=url)

    @classmethod
    def _create_connectivity_operation(cls, data):
        url = data['URL']
        return ConnectivityOp(url=url)


class ResultsStoreFileJSON(ResultsStore):
    def __init__(self, path):
        self.path = path
        self.results = None

    def get_results(self):
        if not self.results:
            try:
                with open(self.path, 'r') as results_file:
                    results_data = json.load(results_file)
                    decoder = ResultsDecoder()
                    self.results = (decoder.decode_json(results_data))
                    return self.results
            except FileNotFoundError:
                self.results = None
                return None
        return self.results

    def write(self, results, append_results=True):
        if not results:
            return

        if append_results:
            self.reload_results()
            self.get_results()
            if self.results:
                all_results = self.results.copy()
                all_results.extend(results)
                results = all_results

        with open(self.path, 'w+') as results_file:
            json.dump(results, results_file, cls=ResultsEncoder)

    def reload_results(self):
        self.results = None


class _RESULT_NAME:
    DNS_LOOKUP = 'DNSLookupResult'
    CONNECTIVITY = 'ConnectivityResult'
    SPEEDTEST = 'SpeedTestResult'
    PING = 'PingResult'


class _ATTR_NAME:
    TIMESTAMP = 'Time'
    URL = 'URL'
    PING_TIMES = 'PingTimes'
    AVERAGE_DOWNLOAD_SPEED_BPS = 'AvgSpeedBps'
    IPV4 = 'IPv4'
    IPV6 = 'IPv6'


class ResultsDecoder:
    def __init__(self):
        self._decoder_for_result = {
            _RESULT_NAME.DNS_LOOKUP: self._decode_dnslookup_result,
            _RESULT_NAME.CONNECTIVITY: self._decode_connectivity_result,
            _RESULT_NAME.PING: self._decode_ping_result,
            _RESULT_NAME.SPEEDTEST: self._decode_speedtest_result
        }

    def decode_json(self, data):
        results = []
        for result_object in data:
            result_name = list(result_object.keys())[0]
            results.append(self._decoder_for_result[result_name](result_object[result_name]))
        return results

    @staticmethod
    def _decode_dnslookup_result(data):
        timestamp = dateutil.parser.parse(data[_ATTR_NAME.TIMESTAMP])
        url = data[_ATTR_NAME.URL]
        ipv4s = set(data[_ATTR_NAME.IPV4])
        ipv6s = set(data[_ATTR_NAME.IPV6])
        return DnsLookupResult(url=url, timestamp=timestamp, ipv4s=ipv4s, ipv6s=ipv6s)

    @staticmethod
    def _decode_ping_result(data):
        timestamp = dateutil.parser.parse(data[_ATTR_NAME.TIMESTAMP])
        url = data[_ATTR_NAME.URL]
        ping_times = data[_ATTR_NAME.PING_TIMES]
        return PingOpResult(url=url, timestamp=timestamp, ping_times=ping_times)

    @staticmethod
    def _decode_speedtest_result(data):
        timestamp = dateutil.parser.parse(data[_ATTR_NAME.TIMESTAMP])
        url = data[_ATTR_NAME.URL]
        average_donwload_speed = data[_ATTR_NAME.AVERAGE_DOWNLOAD_SPEED_BPS]
        return SpeedTestResult(url=url, timestamp=timestamp, average_download_speed=average_donwload_speed)

    @staticmethod
    def _decode_connectivity_result(data):
        ping_result = ResultsDecoder._decode_ping_result(data[_RESULT_NAME.PING])
        speedtest_result = ResultsDecoder._decode_speedtest_result(data[_RESULT_NAME.SPEEDTEST])
        return ConnectivityResult(ping_result=ping_result, speedtest_result=speedtest_result)


class ResultsEncoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.encoder = {
            DnsLookupResult: self._encode_dns_lookup_result,
            PingOpResult: self._encode_ping_result,
            SpeedTestResult: self._encode_speedtest_result,
            ConnectivityResult: self._encode_connectivity_result
        }

    def default(self, o):
        try:
            encoder = self.encoder[type(o)]
        except KeyError:
            raise ValueError("Tried encoding unrecognized type: %s" % type(o))

        return encoder(o)

    @staticmethod
    def _encode_dns_lookup_result(result):
        d = {_RESULT_NAME.DNS_LOOKUP: dict()}
        d[_RESULT_NAME.DNS_LOOKUP][_ATTR_NAME.TIMESTAMP] = result.timestamp.isoformat()
        d[_RESULT_NAME.DNS_LOOKUP][_ATTR_NAME.URL] = result.url
        d[_RESULT_NAME.DNS_LOOKUP][_ATTR_NAME.IPV4] = list(result.ipv4s)
        d[_RESULT_NAME.DNS_LOOKUP][_ATTR_NAME.IPV6] = list(result.ipv6s)
        return d

    @staticmethod
    def _encode_ping_result(result):
        d = {_RESULT_NAME.PING: dict()}
        d[_RESULT_NAME.PING][_ATTR_NAME.TIMESTAMP] = result.timestamp.isoformat()
        d[_RESULT_NAME.PING][_ATTR_NAME.URL] = result.url
        d[_RESULT_NAME.PING][_ATTR_NAME.PING_TIMES] = result.ping_times
        return d

    @staticmethod
    def _encode_speedtest_result(result):
        d = {_RESULT_NAME.SPEEDTEST: dict()}
        d[_RESULT_NAME.SPEEDTEST][_ATTR_NAME.TIMESTAMP] = result.timestamp.isoformat()
        d[_RESULT_NAME.SPEEDTEST][_ATTR_NAME.URL] = result.url
        d[_RESULT_NAME.SPEEDTEST][_ATTR_NAME.AVERAGE_DOWNLOAD_SPEED_BPS] = result.average_download_speed
        return d

    @staticmethod
    def _encode_connectivity_result(result):
        d = {_RESULT_NAME.CONNECTIVITY: dict()}
        d[_RESULT_NAME.CONNECTIVITY].update(ResultsEncoder._encode_speedtest_result(result.speedtest_result))
        d[_RESULT_NAME.CONNECTIVITY].update(ResultsEncoder._encode_ping_result(result.ping_result))
        return d
