#!/usr/bin/env python3
"""
Application entry point script.
"""
import console
from alias import args_t
from arg_parse import Parser
from query_params import QueryParams
from web_scraper import WebScraper


def rfc_search(args: args_t) -> None:
    """
    Perform the RFC specification search and scrape the HTML results.
    """
    params = QueryParams(args.rfc_id, args.keyword if args.keyword else "")
    scraper = WebScraper(params, list_results=(args.list if args.list else False))

    scraper.search()


def main() -> None:
    """
    Application startup function.
    """
    console.setup_console()

    parser = Parser()
    args = parser.parse_args()

    # Invalid arguments, so terminate the app
    if not parser.is_valid() or parser.Args.help:
        exit(1)

    rfc_search(args)
    print()


# Static application entry point
if __name__ == "__main__":
    main()
