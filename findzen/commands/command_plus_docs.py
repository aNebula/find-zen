"""Extend ILCLI Command to include docs from doc-strings."""

from ilcli import Command


class CommandPlusDocs(Command):
    """Extend ILCLI to use doc strings for help/usage error."""
    def __init__(self,
                 parser=None,
                 parent=None,
                 name=None,
                 out=None,
                 err=None) -> None:
        """Override default ILCLI behaviour to include class documentation in command help description."""
        super(CommandPlusDocs, self).__init__(parser, parent, name, out, err)
        self.parser.description = self.__doc__
