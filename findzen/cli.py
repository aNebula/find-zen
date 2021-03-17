"""Entry point for the command findzen CLI."""


from ilcli import Command
from commands.load_data import LoadDataCmd
import logging

logger = logging.getLogger('findzen')

class CommandPlusDocs(Command):
    """Extend ILCLI to use doc strings for help/usage error."""

    def __init__(self, parser=None, parent=None, name=None, out=None, err=None) -> None:
        """Override default ILCLI behaviour to include class documentation in command help description."""
        super(CommandPlusDocs, self).__init__(parser, parent, name, out, err)
        self.parser.description = self.__doc__


class FindZen(CommandPlusDocs):
    """A simple search cli for user, organisation and ticket data."""
    
    subcommands = [
        LoadDataCmd
        ]


def run()-> None:
    exit(FindZen().run())

if __name__ =="__main__":
    run()




    