"""Entry point for cli ticket command."""

from commands.command_plus_docs import CommandPlusDocs
import logging
from file_handler import CacheHandler
import sys
from models.ticket import Ticket
from search import search, search_user_org_by_tickets
from pretty_print import pretty_print_tickets

logger = logging.getLogger('findzen')

class TicketCmd(CommandPlusDocs):
    """Search for ticket by a given field. Returns the ticket details, plus it's user and organization."""
    name="ticket"

    def _init_arguments(self) -> None:
        for field in Ticket.__fields__:
            self.add_argument(f'--{field}', help=f'search for ticket with {field} field' )

    def _run(self, args) -> int:
        try:
            if len(sys.argv) != 4:
                raise BaseException("Wrong arguments: Requires exactly 1 field key and value to search with. Empty values are indicated by ''. ")
            
            search_by_field = sys.argv[2][2:]
            search_by_value = sys.argv[3]
            if search_by_field not in Ticket.__fields__:
                raise BaseException('Wrong arguments: Provided field name is not a field in Tickets data.')
            
            if search_by_field == "id":
                ticket_ids = [search_by_value]
            else:
                ticket_ids  = search('ticket', search_by_field, [search_by_value], True)  
            
            tickets = search('ticket', 'id', ticket_ids)

            if len(tickets) == 0:
                print(f'Ticket with {search_by_field} {search_by_value} not found.')


            tickets_users_orgs = search_user_org_by_tickets(tickets)

            pretty_print_tickets(tickets_users_orgs)

        except BaseException as err:
            logger.error(f'Failed: {err}')
            return 1

        return 0

    def _get_user_org(self, user_id: str, org_id: str):
        
        cache = CacheHandler()
        
        user_cache = cache.read_cache('user_index')
        if user_id in user_cache:
            user = user_cache[user_id]
        else:
            user = None

        org_cache = cache.read_cache('org_index')
        if org_id in org_cache:
            org = org_cache[org_id]
        else:
            org = None
        
        return user, org

