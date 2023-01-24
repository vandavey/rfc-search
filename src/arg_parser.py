"""
Command-line argument parser module.
"""
from argparse import ArgumentParser


class Parser:
    """
    Command-line argument parser.
    """
    def __init__(self) -> None:
        """
        Initialize the object.
        """
        raise NotImplementedError(Parser.__init__)

    def help(self) -> str:
        """
        Get the application help information.
        """
        raise NotImplementedError(self.help)

    def usage(self) -> str:
        """
        Get the application usage information.
        """
        raise NotImplementedError(self.usage)
