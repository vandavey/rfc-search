#!/usr/bin/env python3
"""
Application entry point script.
"""
import console
from alias import args_t, void_t
from arg_parse import Parser


def parse_args() -> tuple[args_t, list[str]]:
    """
    Parse and validate the command-line arguments.
    """
    parser = Parser()
    args = parser.parse_args()

    return args, parser.UnknownArgs


def main() -> void_t:
    """
    Application startup function.
    """
    console.setup_console()
    cl_args, unknown_args = parse_args()

    raise NotImplementedError(main)


# Static application entry point
if __name__ == "__main__":
    main()
