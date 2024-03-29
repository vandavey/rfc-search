"""
RFC specification web crawler module.
"""
import requests
import utils
from requests import Response
from alias import void_t
from query_params import QueryParams
from spec_metadata import SpecMetadata


class Crawler:
    """
    RFC specification web crawler.
    """
    def __init__(self, params: QueryParams) -> None:
        """
        Initialize the object.
        """
        self.Params: QueryParams = params  # Lookup query parameters

    def _send_request(self, url: str) -> Response | void_t:
        """
        Send an HTTP GET request to the server with the underlying query parameters.
        """
        if not utils.valid_url(url):
            raise ValueError(f"Invalid url: {url}")

        response = requests.get(url, self.Params.dict())
        response.close()

        return response

    def crawl(self, url: str) -> SpecMetadata | list[SpecMetadata] | void_t:
        """
        Use the RFC web search functionality to find the specification(s)
        matching the criteria in the underlying query parameters.
        """
        if not utils.valid_url(url):
            raise ValueError(f"Invalid URL: {url}")

        self.Params.validate()
        url = "https://www.rfc-editor.org/search/rfc_search_detail.php"

        # ID search takes precedence over keyword search
        return self.id_search(url) if self.Params.Id else self.keyword_search(url)

    def id_search(self, url: str) -> SpecMetadata | void_t:
        """
        Use the RFC web search functionality to find the specification matching
        the RFC number specified in the underlying query parameters.
        """
        if not self.Params.Id:
            raise RuntimeError("Missing RFC number for which to search")

        raise NotImplementedError(self.id_search)

    def keyword_search(self, url: str) -> list[SpecMetadata] | void_t:
        """
        Use the RFC web search functionality to find the specifications containing
        the RFC title or keyword specified in the underlying query parameters.
        """
        if not self.Params.Title:
            raise RuntimeError("Missing RFC title or keyword for which to search")

        raise NotImplementedError(self.keyword_search)


# Module export symbols
__all__ = ["Crawler"]
