"""
RFC specification metadata module.
"""
import json


class Metadata:
    """
    RFC specification metadata.
    """
    def __init__(self,
                 rfc_id: int = 0,
                 files: dict[str, str] | None = None,
                 title: str = "",
                 authors: str = "",
                 date: str = "",
                 more_info: str = "",
                 status: str = "",
                 page_url: str = ""):
        """
        Initialize the object.
        """
        self.Id: int = rfc_id
        self.Files: dict[str, str] = files if files else {}
        self.Title: str = title
        self.Authors: str = authors
        self.Date: str = date
        self.MoreInfo: str = more_info
        self.Status: str = status
        self.PageUrl: str = page_url

    def __repr__(self) -> str:
        """
        Get the string representation of the specification metadata.
        """
        return f'"rfc{self.Id}": {self.json()}'

    def json(self, indent: int = 4) -> str:
        """
        Get the specification metadata as a JSON string.
        """
        return json.dumps(self.__dict__, indent=abs(indent))


# Module export symbols
__all__ = ["Metadata"]
