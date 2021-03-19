"""Entry point for the command findzen CLI."""

from findzen.commands.command_plus_docs import CommandPlusDocs
from findzen.commands.load_data import LoadDataCmd
from findzen.commands.user_cmd import UserCmd
from findzen.commands.org_cmd import OrgCmd
from findzen.commands.ticket_cmd import TicketCmd
import logging

logger = logging.getLogger('findzen')

class FindZen(CommandPlusDocs):
    """A simple search cli for user, organisation and ticket data."""
    
    subcommands = [
        LoadDataCmd,
        UserCmd,
        OrgCmd,
        TicketCmd
        ]


def run()-> None:
    exit(FindZen().run())

if __name__ =="__main__":
    run()




    