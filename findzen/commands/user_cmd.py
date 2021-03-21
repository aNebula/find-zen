"""Entry point for cli users command."""

from findzen.commands.command_plus_docs import CommandPlusDocs
from findzen.file_handler import CacheHandler
from findzen.models.user import User
from findzen.pretty_print import pretty_print_users
from findzen.utils import search_cache, sanitize_argument
import sys
import logging


logger = logging.getLogger('findzen')


class UserCmd(CommandPlusDocs):
    """Search for user by a given field. Returns the user details, plus organizations and tickets of the user."""
    name='user'

    def _init_arguments(self) -> None:
        for field in User.__fields__:
            self.add_argument(f'--{field}', help=f'search for user with {field} field')

    def _run(self, args) -> int:
        try:
            if len(sys.argv) != 4:
                raise BaseException('Wrong arguments: Requires exactly 1 field key and value to search with. Empty values are indicated by ''. ')

            search_by_field = sys.argv[2][2:]
            search_by_value = sanitize_argument(sys.argv[3])
            if search_by_field not in User.__fields__:
                raise BaseException('Wrong arguments: Provided field name is not a field in Users data.')

            if search_by_field == 'id':
                user_ids = [search_by_value]
            else:
                user_ids  = search_cache('user', search_by_field, [search_by_value])

            users = search_cache('user', 'id', user_ids)

            if len(users)==0:
                print(f'User with {search_by_field} {search_by_value} not found.')
                return 0


            pretty_print_users(users)
            return 0

        except BaseException as err:
            logger.error(f'Failed: {err}')
            return 1