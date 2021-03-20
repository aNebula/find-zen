from findzen.commands.command_plus_docs import CommandPlusDocs
from findzen.file_handler import DataLoader, CacheHandler
from findzen.models.user import User
from findzen.models.org import Organization
from findzen.models.ticket import Ticket
from findzen.indexer import append_or_create, index_builder
import argparse
import logging
from pathlib import Path

logger = logging.getLogger('find_zen')


class LoadDataCmd(CommandPlusDocs):
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
            cache_handler.write_cache(index_builder(users, User))
            cache_handler.write_cache(index_builder(orgs, Organization))
            cache_handler.write_cache(index_builder(tickets, Ticket))

        except BaseException as err:
            logger.error(f'Failed: {err}')
            return 1

        return 0

        index = {}
        for entry in data.dict()["__root__"]:
            index[str(entry["id"])] = entry
        return index


