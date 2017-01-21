from controllers import OperationsController
from store.files import OperationsFile

class NetworkHealthUtility:

    def start(self):
        ops_filepath = '/Users/avihut/Develop/NetHealthUtil/sample/nethealthconf.json'
        operations_controller = OperationsController()
        try:
            operations_controller.operations = OperationsFile(ops_filepath).getOperations()
        except FileNotFoundError:
            print("Could not open file '%s'" % ops_filepath)
        else:
            operations_controller.run()