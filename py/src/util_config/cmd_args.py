from store.files import OperationsStoreFileJSON, ResultsStoreFileJSON
from util_config import UtilConfig, ConfigError
from argparse import ArgumentParser


# nethealth -c conf.json -o results.json

class CmdArgsUtilConfig(UtilConfig):
    def __init__(self):
        super().__init__()
        self.parser = ArgumentParser(description="Run network health diagnostics.")
        self.parser.add_argument(
            '-t', '--tests-file',
            metavar='FILE',
            required=True,
            help='A file that contains network health test instructions',
        )
        self.parser.add_argument(
            '-r', '--results-file',
            metavar='FILE',
            help='A file that will contain the results of the netowrk health tests. '
                 'If the file already contains results, the new health teasts results will be appended to it. '
                 'If the file contains results comparable to the new tests, the difference in perfromance will be '
                 'added to the new results.'
        )
        self.parser.add_argument(
            '-d', '--discard-results',
            action='store_true',
            default=False
        )

    def load(self):
        try:
            args = self.parser.parse_args()
        except SystemExit:
            raise ConfigError()

        try:
            self.store.operations_store = OperationsStoreFileJSON(args.tests_file)
        except FileNotFoundError:
            raise ConfigError(message='Could not open tests file %s' % args.tests_file, displayed_error=False)

        if args.results_file:
            self.store.results_store = ResultsStoreFileJSON(args.results_file)
