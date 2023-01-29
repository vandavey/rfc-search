"""
Command-line argument parser module.
"""
import enum

import utils
from argparse import ArgumentParser
from enum import IntEnum
from alias import any_t, args_t, void_t


@enum.unique
class ArgError(IntEnum):
    """
    Command-line argument error type.
    """
    NO_ERROR = 0          # No errors occurred
    UNRECOGNIZED = 1      # Unrecognized argument(s)
    MISSING_REQUIRED = 2  # Required argument missing
    INVALID_COMBO = 3     # Invalid argument combination
    INVALID_VALUE = 4     # Invalid argument value


@enum.unique
class ParseResult(IntEnum):
    """
    Command-line argument parser parsing results status.
    """
    INCOMPLETE = 0  # Parsing incomplete
    VALID = 1       # Arguments are valid
    INVALID = 2     # Arguments are invalid
    HELP = 3        # Help flag was parsed


class Parser:
    """
    Command-line argument parser.
    """
    def __init__(self) -> None:
        """
        Initialize the object.
        """
        self.Args: args_t = args_t()
        self.UnknownArgs: list[str] = list[str]()

        self._Parser: ArgumentParser = ArgumentParser(add_help=False)
        self._Status: ParseResult = ParseResult.INCOMPLETE

        self._setup_args()

    @staticmethod
    def _app_usage() -> str:
        """
        Get the application app_usage information.
        """
        return f"Usage: {utils.app_name()} [OPTIONS] RFC_ID"

    @staticmethod
    def help_msg() -> str:
        """
        Get the application help information.
        """
        help_lines = [
            f"{utils.app_name()} ({utils.repo_url()})",
            f"{Parser._app_usage()}\n",
            f"RFC specification search application\n",
            f"Positional Arguments:",
            f"  RFC_ID                   RFC specification ID number\n",
            f"Optional Arguments:",
            f"  -h/-?, --help            Show this help message and exit",
            f"  -v,    --verbose         Enable verbose console output",
            f"  -k,    --keyword TERM    Perform the RFC search using a keyword",
            f"  -l,    --list            Get a list of RFC specifications\n",
            f"Usage Examples:",
            f"  rfc-search.py 9293",
            f"  rfc-search.py -l -k TCP",
            f"  rfc-search.py --keyword TCP"
        ]
        return "\n".join(help_lines)

    def _add_pos_arg_spec(self, name: str, arg_t: type, **kwargs: any_t) -> void_t:
        """
        Attach a positional argument specification to the underlying argument parser.
        """
        if not name or name.startswith("-"):
            raise ValueError(f"Invalid positional argument name: '{name}'")

        self._Parser.add_argument(name, type=arg_t, **kwargs)

    def _add_opt_arg_spec(self,
                          name: str,
                          arg_t: type,
                          aliases: list[str],
                          **kwargs: any_t) -> void_t:
        """
        Attach an optional argument specification to the underlying argument parser.
        """
        if not name or name.startswith("-"):
            raise ValueError(f"Invalid argument name: '{name}'")

        for alias in aliases:
            if len(alias) == 0:
                raise ValueError(f"At least one argument name alias is required")

            if len(alias) != 1 or alias == "-":
                raise ValueError("Argument alias must be a single letter")

        names = [*[f"-{a}" for a in aliases], f"--{name}"]
        self._Parser.add_argument(*names, type=arg_t, **kwargs)

    def _setup_args(self) -> void_t:
        """
        Configure the underlying argument parser argument specifications.
        """
        self._add_pos_arg_spec("rfc_id", int, nargs="?")
        self._add_opt_arg_spec("help", bool, ["h", "?"])
        self._add_opt_arg_spec("verbose", bool, ["v"])
        self._add_opt_arg_spec("keyword", str, ["k"])
        self._add_opt_arg_spec("list", bool, ["l"])

    def parse_args(self) -> tuple[args_t, ParseResult]:
        """
        Parse the application command-line arguments.
        """
        self.Args, self.UnknownArgs = self._Parser.parse_known_args()
        return self.Args, self._Status


# Module export symbols
__all__ = ["ArgError", "Parser", "ParseResult"]
