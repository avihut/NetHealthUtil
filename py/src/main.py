from controllers import OperationsController
from util_config import ConfigError
import sys


class NetworkHealthUtility:
    def __init__(self, config=None, view_system=None):
        self.config = config
        self.view = view_system

    def start(self):
        try:
            self.config.load()
        except ConfigError as e:
            if not e.displayed_error:
                print("Configuration error: %s" % e.message)
            sys.exit(1)

        self.operations_controller = OperationsController(
            operations=self.config.store.operations_store.get_operations(),
            previous_results=self.config.store.results_store.get_results()
        )
        self.operations_controller.run()

        print('\nStoring results')
        self.config.store.results_store.write(self.operations_controller.results)
