class OperationsStore:
    def get_operations(self):
        pass


class ResultsStore:
    def get_results(self):
        pass

    def write_results(self, results):
        pass


class Store:
    def __init__(self, configuration_store=None, results_store=None):
        self.configuration_store = configuration_store
        self.results_store = results_store
