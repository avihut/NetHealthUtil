from operations import DnsLookupOp, ConnectivityOp
import json

class OperationsFile:
    def __init__(self, path):
        self.path = path
        self.instantiate = {
            'DnsLookup': self._create_dns_lookup_operation,
            'Connectivity': self._create_connectivity_operation
        }

    def getOperations(self):
        operations = []
        with open(self.path) as operations_file:
            operations_data = json.load(operations_file)
            for operation_config in operations_data:
                operation_name = list(operation_config.keys())[0]
                args = operation_config[operation_name]
                operations.append(self.instantiate[operation_name](args))
        return operations

    @classmethod
    def _create_dns_lookup_operation(cls, args):
        args = list(args.values())
        return DnsLookupOp(*args)

    @classmethod
    def _create_connectivity_operation(cls, args):
        args = list(args.values())
        return ConnectivityOp(*args)