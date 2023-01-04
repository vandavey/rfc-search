#
#  crawler.py
#  ----------
#  RFC specification web crawler module.
#
import requests
from requests import Response
from . import utils
from .query_params import QueryParams
from .spec_metadata import SpecMetadata


class Crawler:
    """
    RFC specification web crawler.
    """
    def __init__(self, params: QueryParams):
        """
        Initialize the object.
        """
        self.Params: QueryParams = params  # Lookup query parameters

    def _send_request(self, url: str) -> Response | None:
        """
        Send an HTTP GET request to the server with the underlying query parameters.
        """
        if not utils.valid_url(url):
            raise ValueError(f"Invalid url: {url}")

        response = requests.get(url, self.params.dict())
        response.close()

        return response

    def id_search(self, url: str) -> SpecMetadata | None:
        """
        Use the RFC web search functionality to find the specification matching
        the RFC number specified in the underlying query parameters.
        """
        if not self.Params.Id:
            raise RuntimeError("Missing RFC number for which to search")

        raise NotImplementedError(self.id_search)

    def keyword_search(self, url: str) -> list[SpecMetadata] | None:
        """
        Use the RFC web search functionality to find the specifications containing
        the RFC title or keyword specified in the underlying query parameters.
        """
        if not self.Params.Title:
            raise RuntimeError("Missing RFC title or keyword for which to search")

        raise NotImplementedError(self.keyword_search)

    def crawl(self, url: str) -> SpecMetadata | list[SpecMetadata] | None:
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
