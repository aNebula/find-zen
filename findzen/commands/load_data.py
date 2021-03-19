from findzen.commands.command_plus_docs import CommandPlusDocs
from findzen.file_handler import DataLoader, CacheHandler
from findzen.models.user import User
from findzen.models.org import Organization
from findzen.models.ticket import Ticket
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
            cache_handler.write_cache(self._index_builder(users, User))
            cache_handler.write_cache(self._index_builder(orgs, Organization))
            cache_handler.write_cache(self._index_builder(tickets, Ticket))

        except BaseException as err:
            logger.error(f'Failed: {err}')
            return 1

        return 0

        index = {}
        for entry in data.dict()["__root__"]:
            index[str(entry["id"])] = entry
        return index

    def _append_or_create(self, dict, key, value):
        #if dict is None:
            #dict = {}

        if key in dict:
            dict[key].append(value)
            return dict
        dict[key] = [value]
        return dict

    def _index_builder(self, data, data_type):
        all_indexes = {}
        key_prefix = f'{data_type.__name__.lower()}_index_by_'
        for key in data_type.__fields__:
            all_indexes[f'{key_prefix}{key}']= {}

        for entry in data.dict()["__root__"]:
            for key in data_type.__fields__:
                key_string = f'{key_prefix}{key}'
                if key == "id":
                    all_indexes[key_string][str(entry[key])] =  entry
                    continue
                if key == "tags":
                    for tag in entry["tags"]:
                       all_indexes[key_string]=  self._append_or_create(all_indexes[key_string], str(tag), entry["id"])
                    continue
                if key == "domain_names":
                    for domain_name in entry["domain_names"]:
                       all_indexes[key_string]=  self._append_or_create(all_indexes[key_string], str(domain_name), entry["id"])
                    continue

                all_indexes[key_string]= self._append_or_create(all_indexes[key_string], str(entry[key]), entry["id"])
        
        return all_indexes

