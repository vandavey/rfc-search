"""
RFC specification web scraper module.
"""
from typing import Any

from bs4 import BeautifulSoup

import requests
from requests import Response

import console
import utils
from query_params import QueryParams
from metadata import Metadata
from utils import MetaField

# TODO: Implement verbose output logic

_ANCHOR = "a"
_DIVISION = "div"
_HYPERTEXT_REF = "href"
_LIST_ITEM = "li"
_TABLE = "table"
_TABLE_DATA = "td"
_TABLE_HEADER = "th"
_TABLE_ROW = "tr"

_SEARCH_URI = "https://www.rfc-editor.org/search/rfc_search_detail.php"


class WebScraper:
    """
    RFC specification web scraper.
    """
    def __init__(self, params: QueryParams, list_results: bool = False) -> None:
        """
        Initialize the object.
        """
        self.Params: QueryParams = params
        self.ListResults: bool = list_results
        self.Valid: bool = True

    def search(self) -> None:
        """
        Use the RFC web search functionality to find the specification(s)
        matching the criteria in the underlying query parameters.
        """
        self.Params.validate()
        resp = self._send_request(_SEARCH_URI)

        # Search web request succeeded
        if resp.ok:
            metadata_list = self._extract_metadata(resp.text)

            # Display a list of matching specifications
            if len(metadata_list) > 1 or self.ListResults:
                for rfc_id, title, date in self._make_table(metadata_list):
                    title = f"{title[:35]}..." if len(title) > 35 else title
                    print("{:<9} {:<41} {}".format(rfc_id, title, date))

            # Display the content of the matching specification
            elif len(metadata_list) == 1:
                print(self._spec_content(metadata_list[0].Files["ASCII"]))

        # Search web request failed
        else:
            console.error_ln(f"Web request failure: HTTP {resp.status_code}")

    @staticmethod
    def _extract_doc_links(anchors: list[BeautifulSoup]) -> dict[str, str]:
        """
        Get a dictionary mapping the available RFC document types
        and their URLs from the given table row element.
        """
        file_dict = dict[str, str]()

        for anchor_data in anchors[MetaField.FILES].find_all(_ANCHOR):
            file_dict[anchor_data.text] = anchor_data.attrs[_HYPERTEXT_REF]

        return file_dict

    @staticmethod
    def _extract_spec_metadata(table_row: BeautifulSoup) -> Metadata | None:
        """
        Extract RFC specification metadata from the given table row element.
        """
        cells = table_row.find_all(_TABLE_DATA)
        spec_url_data = table_row.find(_ANCHOR)

        metadata = None

        if cells and len(cells) == 7:
            metadata = Metadata(rfc_id=int(spec_url_data.text.strip().split()[1]),
                                files=WebScraper._extract_doc_links(cells),
                                title=cells[MetaField.TITLE].text.strip(),
                                authors=cells[MetaField.AUTHORS].text.strip(),
                                date=cells[MetaField.DATE].text.strip(),
                                more_info=cells[MetaField.MORE_INFO].text.strip(),
                                status=cells[MetaField.STATUS].text.strip(),
                                page_url=spec_url_data.attrs[_HYPERTEXT_REF])

        return metadata

    @staticmethod
    def _make_table(table_rows: list[Metadata]) -> list[tuple[Any, Any, Any]]:
        """
        Create a list of RFC specification search results from the
        given list of specification metadata.
        """
        table = [
            ("NUMBER", "TITLE", "DATE"),
            ("=" * 6, "=" * 5, "=" * 4),
            *[(r.Id, r.Title, r.Date) for r in table_rows]
        ]
        return table

    def _spec_content(self, url: str) -> str:
        """
        Extract the content of an RFC specification by making a web
        request to the given URL.
        """
        if not utils.valid_url(url):
            raise ValueError(f"Invalid URL specified: '{url}'")

        spec_content = ""
        resp = self._send_request(url)

        self.Valid = resp.ok

        if self.Valid:
            spec_content = resp.text
        else:
            console.error_ln(f"Web request failure: HTTP {resp.status_code}")

        return spec_content

    def _extract_metadata(self, raw_html_data) -> list[Metadata]:
        """
        Extract RFC specification metadata from the given HTML search results data.
        """
        if not raw_html_data:
            raise ValueError(f"The given HTML data cannot be null or empty")

        metadata_list = list[Metadata]()
        html_data = BeautifulSoup(raw_html_data, "html.parser")
        table_data = html_data.find(_TABLE, class_="gridtable")

        # Extract specification metadata from each table row
        if table_data:
            for table_row in table_data.find_all(_TABLE_ROW):
                if not table_row.find(_TABLE_HEADER):
                    metadata = self._extract_spec_metadata(table_row)

                    if metadata:
                        metadata_list.append(metadata)

        # Web search error(s) occurred
        elif html_data.find(_DIVISION, class_="errors"):
            errors = html_data.find_all(_LIST_ITEM)

            for error_data in errors:
                self.Valid = False
                console.error_ln(error_data.text.strip())

        # No matching specifications were found
        else:
            self.Valid = False
            console.warn_ln(f"No matching RFC specifications were found")

        return metadata_list

    def _send_request(self, url: str) -> Response | None:
        """
        Send an HTTP GET request to the server with the underlying query parameters.
        """
        if not utils.valid_url(url):
            raise ValueError(f"Invalid URL specified: '{url}'")

        resp = requests.get(url, self.Params.dict())
        resp.close()

        return resp


# Module export symbols
__all__ = ["WebScraper"]
