from controllers import OperationsController
from store.files import OperationsStoreFileJSON


class NetworkHealthUtility:
    def __init__(self, config=None, view_system=None):
        self.config = config
        self.view = view_system

    def start(self):
        e = self.config.validate()
        if e:
            print("Configuration error")
            return

        ops_filepath = '/Users/avihut/Develop/NetHealthUtil/sample/nethealthconf.json'
        operations_controller = OperationsController()
        try:
            operations_controller.operations = OperationsStoreFileJSON(ops_filepath).get_operations()
        except FileNotFoundError:
            print("Could not open file '%s'" % ops_filepath)
        else:
            operations_controller.run()
