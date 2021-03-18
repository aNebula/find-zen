from ilcli import Command
import argparse
import logging
from pathlib import Path
from file_handler import DataLoader, CacheHandler

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
            dir_path = Path(args.path)
            data_loader = DataLoader('json', dir_path)
            users, orgs, tickets = data_loader.load()
            logger.info("Data loaded into memory")

            cache_handler = CacheHandler()
            cache_handler.write_cache("user_index", self._index_builder(users))
            cache_handler.write_cache("orgs_index", self._index_builder(orgs))
            cache_handler.write_cache("tickets_index", self._index_builder(tickets))

        except BaseException as err:
            logger.error(f'Failed: {err}')
            return 1

        return 0


    def _index_builder(self, data):
        index = {}
        for entry in data.dict()["__root__"]:
            index[str(entry["id"])] = entry
        return index