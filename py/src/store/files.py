from operations import DnsLookupOp, ConnectivityOp
from store import OperationsStore
import json


class OperationsStoreFileJSON(OperationsStore):
    def __init__(self, path):
        self.path = path
        self.instantiate = {
            'DnsLookup': self._create_dns_lookup_operation,
            'Connectivity': self._create_connectivity_operation
        }

    def get_operations(self):
        operations = []
        with open(self.path) as operations_file:
            operations_data = json.load(operations_file)
            for operation_config in operations_data:
                operation_name = list(operation_config.keys())[0]
                args = operation_config[operation_name]
                operations.append(self.instantiate[operation_name](args))
        return operations

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
