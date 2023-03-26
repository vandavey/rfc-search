"""
Command-line argument parser module.
"""
import argparse
import enum
import console
import utils
from alias import any_t, args_t, void_t


# Parsing error occurred
_error_occurred: bool = False


@enum.unique
class ArgError(enum.StrEnum):
    """
    Command-line argument error type.
    """
    NO_ERROR = "No argument parsing errors occurred"
    UNRECOGNIZED = "Unrecognized argument(s): {}"
    MISSING_REQUIRED = "One of the following arguments is required: {}, {}"
    INVALID_COMBO = "Invalid argument combination: {}"
    INVALID_VALUE = "Invalid value for argument '{}': {}"


class ArgumentParser(argparse.ArgumentParser):
    """
    Customized standard library command-line argument parser.
    """
    def error(self, message: str) -> void_t:
        """
        Override the default argument error handling so that it can
        be handled by the user-defined argument parser.
        """
        global _error_occurred
        _error_occurred = True


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
        self._Valid: bool = False

        self._setup_args()

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
            f"  rfc-search.py --keyword TCP\n"
        ]
        return "\n".join(help_lines)

    @staticmethod
    def _app_usage() -> str:
        """
        Get the application usage information.
        """
        return f"Usage: {utils.app_name()} [-?hlv] [-k KEYWORD] [RFC_ID]"

    @staticmethod
    def _fmt_error_msg(error: ArgError, *args: any_t) -> str:
        """
        Format an argument error message using the specified arguments.
        """
        return error.value.format(*args)

    @staticmethod
    def _print_error(error: ArgError, *args: any_t) -> void_t:
        """
        Write the application usage to the standard output stream and
        write an error message to the standard error stream.
        """
        print(Parser._app_usage())
        console.error_ln(f"{error.value.format(*args)}\n")

    def parse_args(self) -> args_t:
        """
        Parse the application command-line arguments.
        """
        self.Args, self.UnknownArgs = self._Parser.parse_known_args()
        self.validate()

        return self.Args

    def is_valid(self) -> bool:
        """
        Determine whether the parsed underlying command-line arguments are valid.
        """
        return self._Valid

    def validate(self) -> void_t:
        """
        Determine whether the parsed underlying command-line arguments are valid.
        """
        if not _error_occurred and (self.Args.help or not self._args_provided()):
            print(Parser.help_msg())
            self._Valid = True

        else:
            if self.UnknownArgs:
                Parser._print_error(ArgError.UNRECOGNIZED,
                                    ", ".join(self.UnknownArgs))

            elif not self.Args.rfc_id and not self.Args.keyword:
                Parser._print_error(ArgError.MISSING_REQUIRED,
                                    "-k/--keyword TERM",
                                    "RFC_ID")

            elif self.Args.rfc_id and self.Args.keyword:
                Parser._print_error(ArgError.INVALID_COMBO,
                                    "-k/--keyword TERM, RFC_ID")
            self._Valid = False

    def _args_provided(self) -> bool:
        """
        Determine whether any command-line arguments were provided.
        """
        args_list = [
            self.Args.help,
            self.Args.keyword,
            self.Args.list,
            self.Args.rfc_id,
            self.Args.verbose
        ]
        return not all([not a for a in args_list])

    def _setup_args(self) -> void_t:
        """
        Configure the underlying argument parser argument specifications.
        """
        self._Parser.add_argument("rfc_id", type=int, nargs="?")
        self._Parser.add_argument("-h", "-?", "--help", action="store_true")
        self._Parser.add_argument("-v", "--verbose", action="store_true")
        self._Parser.add_argument("-k", "--keyword", type=str)
        self._Parser.add_argument("-l", "--list", action="store_true")


# Module export symbols
__all__ = ["ArgError", "Parser"]
