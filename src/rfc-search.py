#!/usr/bin/env python3
"""
Application entry point script.
"""
import console  # type: ignore


def main() -> None:
    """
    Application startup function.
    """
    console.setup_console()
    raise NotImplementedError(main)


# Static application entry point
if __name__ == "__main__":
    main()
