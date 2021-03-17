from ilcli import Command
import argparse
import logging

logger = logging.getLogger('find_zen')


class LoadDataCmd(Command):
    """Load data for search - build index for the data and save in cache for quicker search."""
    name = 'load'

    def _init_arguments(self) -> None:
        self.add_argument(
            "path", 
            help="Path to the data directory, containing all 3 of users.json, organizations.json and tickets.json")


    def _run(self, args: argparse.Namespace) -> int:
        try:
            logger.debug("Hello World")

        except BaseException as err:
            logger.error(f'Failed: {err}')
            return 1

        return 0