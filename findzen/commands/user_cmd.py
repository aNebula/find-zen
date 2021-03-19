"""Entry point for cli users command."""

from commands.command_plus_docs import CommandPlusDocs
import logging
from file_handler import CacheHandler
import sys
from models.user import User
from search import search, search_org_ticket_by_users
from pretty_print import pretty_print_users

logger = logging.getLogger('findzen')

class UserCmd(CommandPlusDocs):
    """Search for user by a given field. Returns the user details, plus organizations and tickets of the user."""
    name="user"

    def _init_arguments(self) -> None:
        for field in User.__fields__:
            self.add_argument(f'--{field}', help=f'search for user with {field} field')

    def _run(self, args) -> int:
        try:
            if len(sys.argv) != 4:
                raise BaseException("Wrong arguments: Requires exactly 1 field key and value to search with. Empty values are indicated by ''. ")

            search_by_field = sys.argv[2][2:]
            search_by_value = sys.argv[3]
            if search_by_field not in User.__fields__:
                raise BaseException('Wrong arguments: Provided field name is not a field in Users data.')

            if search_by_field == "id":
                user_ids = [search_by_value]
            else:
                user_ids  = search('user', search_by_field, [search_by_value], True)

            users = search('user', "id", user_ids)


            if len(users) == 0:
                print(f'User with {search_by_field} {search_by_value} not found.')
                return 0
            

            # org_ids = [user["organization_id"] for user in users]
            # orgs =search('organization', "id", org_ids)
            # ticket_ids = search('ticket', "submitter_id", user_ids)
            # tickets = [search('ticket', 'id', ticket_id) for ticket_id in ticket_ids]

            # print_objects = []
            # for idx,user in enumerate(users):
            #     obj = {
            #         "user": user,
            #         "org": orgs[idx]['name'],
            #         "tickets": [ticket["subject"] for ticket in tickets[idx]]
            #     }
            #     print_objects.append(obj)
            
            users_orgs_tickets = search_org_ticket_by_users(users)

            pretty_print_users(users_orgs_tickets)
            return 0

        except BaseException as err:
            logger.error(f'Failed: {err}')
            return 1