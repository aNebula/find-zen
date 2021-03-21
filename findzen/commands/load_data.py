"""Command to load data for search - creates indexes and saves cache for faster retrieval."""
from findzen.commands.command_plus_docs import CommandPlusDocs
from findzen.file_handler import DataLoader, CacheHandler
from findzen.models.user import User
from findzen.models.org import Organization
from findzen.models.ticket import Ticket
from findzen.indexer import index_builder, populate_ticket_index_with_user_org, populate_user_index_with_org_tickets, populated_org_index_with_users_tickets
import argparse
import logging
from pathlib import Path

logger = logging.getLogger('find_zen')


class LoadDataCmd(CommandPlusDocs):
    """Load data for search - build index for the data and save in cache for quicker search."""
    name = 'load'

    def _init_arguments(self) -> None:
        self.add_argument(
            'path', 
            help='Path to the data directory, containing all 3 of users.json, organizations.json and tickets.json')


    def _run(self, args: argparse.Namespace) -> int:
        try:
            dir_path = Path(args.path)
            data_loader = DataLoader('json', dir_path)
            users, orgs, tickets = data_loader.load()
            logger.info('Data loaded into memory')

            # Build initial index - these indexes do not contain the other associated entities yet.
            user_index = index_builder(users, User)
            org_index = index_builder(orgs, Organization)
            ticket_index = index_builder(tickets, Ticket)

            # Use the current index to cross link entities. E.g. User -> Org obj, User-> Ticket Obj
            org_index = populated_org_index_with_users_tickets(user_index, org_index, ticket_index)
            user_index = populate_user_index_with_org_tickets(user_index, org_index, ticket_index)
            ticket_index = populate_ticket_index_with_user_org(user_index, org_index, ticket_index)

            # save cache
            cache_handler = CacheHandler()
            cache_handler.write_cache(user_index)
            cache_handler.write_cache(org_index)
            cache_handler.write_cache(ticket_index)


        except BaseException as err:
            logger.error(f'Failed: {err}')
            return 1

        return 0


