class OperationsStore:
    def get_operations(self):
        pass


class ResultsStore:
    def get_results(self):
        pass

    def write(self, results):
        pass


class Store:
    def __init__(self, operations_store=None, results_store=None):
        self.operations_store = operations_store
        self.results_store = results_store
