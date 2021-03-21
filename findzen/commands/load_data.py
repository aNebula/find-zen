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
            "path", 
            help="Path to the data directory, containing all 3 of users.json, organizations.json and tickets.json")


    def _run(self, args: argparse.Namespace) -> int:
        try:
            dir_path = Path(args.path)
            data_loader = DataLoader('json', dir_path)
            users, orgs, tickets = data_loader.load()
            logger.info("Data loaded into memory")

            user_index = index_builder(users, User)
            org_index = index_builder(orgs, Organization)
            ticket_index = index_builder(tickets, Ticket)

            # org_index_by_id = org_index["organization_index_by_id"]
            # user_index_by_id = user_index["user_index_by_id"]
            # ticket_index_by_id = ticket_index["ticket_index_by_id"]

            
            # for org_id in org_index_by_id:
            #     user_ids = fetch_if_key(user_index["user_index_by_organization_id"],org_id)
            #     users = []
            #     for user_id in user_ids:
            #         users.append(fetch_if_key(user_index_by_id,user_id))
            #     org_index["organization_index_by_id"][org_id]["users"] = users
                
            #     ticket_ids = fetch_if_key(ticket_index["ticket_index_by_organization_id"],org_id)
            #     tickets = []
            #     for ticket_id in ticket_ids:
            #         tickets.append(fetch_if_key(ticket_index_by_id, ticket_id))
            #     org_index["organization_index_by_id"][org_id]["tickets"] = tickets

            # for user_id in user_index_by_id:
            #     # a user belongs to one organization
            #     org_id = user_index_by_id[user_id]["organization_id"]
            #     if org_id is None:
            #         user_index["user_index_by_id"][user_id]["organization"] = []
            #     else:
            #         user_index["user_index_by_id"][user_id]["organization"] = fetch_if_key(org_index_by_id,org_id)
                
            #     ticket_ids = fetch_if_key(ticket_index["ticket_index_by_submitter_id"], user_id)
            #     tickets = []
            #     for ticket_id in ticket_ids:
            #         tickets.append(fetch_if_key(ticket_index_by_id,ticket_id))
            #     user_index["user_index_by_id"][user_id]["tickets"] = tickets

            # for ticket_id in ticket_index_by_id:
            #     user_id = ticket_index_by_id[ticket_id]["submitter_id"]
            #     if user_id is None:
            #         ticket_index["ticket_index_by_id"][ticket_id]["user"] = []
            #     else:
            #         ticket_index["ticket_index_by_id"][ticket_id]["user"] = fetch_if_key(user_index_by_id, user_id)

            #     org_id = ticket_index_by_id[ticket_id]["organization_id"]
            #     if org_id is None:
            #         ticket_index["ticket_index_by_id"][ticket_id]["organization"] = []
            #     else:
            #         ticket_index["ticket_index_by_id"][ticket_id]["organization"] = fetch_if_key(org_index_by_id, org_id)

            org_index = populated_org_index_with_users_tickets(user_index, org_index, ticket_index)
            user_index = populate_user_index_with_org_tickets(user_index, org_index, ticket_index)
            ticket_index = populate_ticket_index_with_user_org(user_index, org_index, ticket_index)


            cache_handler = CacheHandler()
            cache_handler.write_cache(user_index)
            cache_handler.write_cache(org_index)
            cache_handler.write_cache(ticket_index)


        except BaseException as err:
            logger.error(f'Failed: {err}')
            return 1

        return 0

        index = {}
        for entry in data.dict()["__root__"]:
            index[str(entry["id"])] = entry
        return index


