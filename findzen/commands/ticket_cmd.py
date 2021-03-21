"""Entry point for cli ticket command."""

from findzen.commands.command_plus_docs import CommandPlusDocs
from findzen.models.ticket import Ticket
from findzen.pretty_print import pretty_print_tickets
from findzen.utils import search_cache, sanitize_argument
import sys
import logging

logger = logging.getLogger('findzen')


class TicketCmd(CommandPlusDocs):
    """Search for ticket by a given field. Returns the ticket details, plus it's user and organization."""

    name = 'ticket'

    def _init_arguments(self) -> None:
        for field in Ticket.__fields__:
            self.add_argument(f'--{field}',
                              help=f'search for ticket with {field} field')

    def _run(self, args) -> int:
        try:
            if len(sys.argv) != 4:
                raise BaseException(
                    'Wrong arguments: Requires exactly 1 field key and value to search with. Empty values are indicated by '
                    '. ')

            search_by_field = sys.argv[2][2:]
            search_by_value = sanitize_argument(sys.argv[3])
            if search_by_field not in Ticket.__fields__:
                raise BaseException(
                    'Wrong arguments: Provided field name is not a field in Tickets data.'
                )

            if search_by_field == 'id':
                ticket_ids = [search_by_value]
            else:
                ticket_ids = search_cache('ticket', search_by_field,
                                          [search_by_value])

            tickets = search_cache('ticket', 'id', ticket_ids)

            if len(tickets) == 0:
                print(
                    f'Ticket with {search_by_field} {search_by_value} not found.'
                )
                return 0

            pretty_print_tickets(tickets)

        except BaseException as err:
            logger.error(f'Failed: {err}')
            return 1

        return 0
