"""Entry point for cli orgatization command."""

from commands.command_plus_docs import CommandPlusDocs
import logging
from file_handler import CacheHandler
import sys
from models.org import Organization
from search import search, search_user_ticket
from pretty_print import pretty_print_orgs

logger = logging.getLogger('findzen')

class OrgCmd(CommandPlusDocs):
    """Search for organization by a given field. Returns the organization details, plus it's users and tickets."""
    name="organization"

    def _init_arguments(self) -> None:
        for field in Organization.__fields__:
            self.add_argument(f'--{field}', help=f'search for organization with {field} field')

    def _run(self, args) -> int:
        try:
            if len(sys.argv) != 4:
                raise BaseException("Wrong arguments: Requires exactly 1 field key and value to search with. Empty values are indicated by ''. ")
            
            search_by_field = sys.argv[2][2:]
            search_by_value = sys.argv[3]
            if search_by_field not in Organization.__fields__:
                raise BaseException('Wrong arguments: Provided field name is not a field in Organizations data.')

            if search_by_field == "id":
                org_ids = [search_by_value]
            else:
                org_ids  = search('organization', search_by_field, [search_by_value], True)  

            orgs = search('organization', 'id', org_ids)

            if len(orgs) == 0:
                print(f'Organization with {search_by_field} {search_by_value} not found.')

            orgs_users_tickets = search_user_ticket(orgs)

            pretty_print_orgs(orgs_users_tickets)

        except BaseException as err:
            logger.error(f'Failed: {err}')
            return 1

        return 0