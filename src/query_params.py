"""
HTTP RFC specification lookup query parameters module.
"""
import enum
from datetime import datetime
from utils import MetaFieldName


@enum.unique
class Sorting(enum.StrEnum):
    """
    RFC specification search results sorting direction.
    """
    ASCENDING = "ASC"
    DESCENDING = "DESC"


class QueryParams:
    """
    HTTP RFC specification lookup query parameters.
    """
    def __init__(self,
                 rfc_id: int,
                 title: str,
                 from_year: int = 1968,
                 to_year: int = datetime.now().year,
                 sort_by: MetaFieldName = MetaFieldName.ID,
                 sorting: Sorting = Sorting.ASCENDING) -> None:
        """
        Initialize the object.
        """
        self.Id: int = rfc_id
        self.Title: str = title
        self.FromYear: int = from_year
        self.ToYear: int = to_year
        self.SortBy: MetaFieldName = sort_by
        self.Sorting: Sorting = sorting

        if self.FromYear < 1968:
            self.FromYear = 1968

        if self.ToYear > datetime.now().year:
            self.ToYear = datetime.now().year

        self.validate()

    def __repr__(self) -> str:
        """
        Get the string representation of the object.
        """
        return str(self.__dir__)

    def dict(self) -> dict[str, str]:
        """
        Get a dictionary of the object to use in RFC lookups.
        """
        return {
            "from_month": "January",
            "from_year": str(self.FromYear),
            "page": "All",
            "pub_date_type": "range",
            "pubstatus[]": "Any",
            "rfc": str(self.Id) if self.Id else "",
            "sorting": str(self.Sorting),
            "sortkey": str(self.SortBy),
            "title": self.Title,
            "to_month": "December",
            "to_year": str(self.ToYear)
        }

    def validate(self) -> None:
        """
        Validate the underlying query parameters.
        """
        if not self.Id and not self.Title:
            error_msg = f"RFC specification number or title must be specified"
            raise RuntimeError(error_msg)

        if self.SortBy not in [n for n in MetaFieldName]:
            fields = ", ".join([f"'{n}'" for n in MetaFieldName])
            raise RuntimeError(f"Invalid sort field, valid fields include {fields}")


# Module export symbols
__all__ = ["QueryParams"]
