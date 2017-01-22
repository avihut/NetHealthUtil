from controllers import OperationsController
from store.files import OperationsStoreFileJSON
from util_config import ConfigValidationError
import sys


class NetworkHealthUtility:
    def __init__(self, config=None, view_system=None):
        self.config = config
        self.view = view_system
        self.operations_controller = OperationsController()

    def start(self):
        try:
            self.config.load()
        except ConfigValidationError as e:
            if not e.displayed_error:
                print("Configuration error")
            sys.exit(1)

        self.operations_controller.operations = self.config.store.operations_store.get_operations()
        self.operations_controller.run()
