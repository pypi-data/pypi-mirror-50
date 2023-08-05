class CliException(Exception):
    """ Base class for IkCli exceptions"""

    @property
    def message(self):
        """ return the error's first arg """
        return self.args[0]
