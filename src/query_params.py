"""
HTTP RFC specification lookup query parameters module.
"""
from datetime import datetime
from .utils import RfcFieldName


class QueryParams:
    """
    HTTP RFC specification lookup query parameters.
    """
    def __init__(self,
                 from_yr: int,
                 to_yr: int,
                 rfc_id: int = 0,
                 title: str = "",
                 page: int = 0,
                 sort_by: RfcFieldName = RfcFieldName.ID,
                 sort_dir: str = "ASC") -> None:
        """
        Initialize the object.
        """
        self.Id: int = rfc_id          # Specification ID
        self.Title: str = title        # Specification title
        self.FromYear: int = from_yr   # Specification published after year
        self.ToYear: int = to_yr       # Specification published to year
        self.Page: int = page          # Number of result pages to include
        self.Sort: str = str(sort_by)  # Field by which to sort results
        self.SortDir: str = sort_dir   # Results sorting direction ('ASC', 'DESC')

        if self.FromYear < 1968:
            self.FromYear = 1968

        if self.ToYear > datetime.now().year:
            self.ToYear = datetime.now().year

        self.validate()

    def __repr__(self):
        """
        Get the string representation of the object.
        """
        return str(self.__dir__)

    def dict(self) -> dict[str, str]:
        """
        Get a dictionary of the object to use in RFC lookups.
        """
        return {
            "rfc": str(self.Id) if self.Id else str(),
            "title": self.Title,
            "from_year": str(self.FromYear),
            "to_year": str(self.ToYear),
            "page": str(abs(self.Page)) if self.Page else "All",
            "sortkey": self.Sort,
            "sorting": self.SortDir,
            "pubstatus[]": "Any",
            "pub_date_type": "range",
            "from_month": "January",
            "to_month": "December"
        }

    def validate(self) -> None:
        """
        Validate the underlying query parameters.
        """
        if not self.Id and not self.Title:
            error_msg = f"RFC specification number or title must be specified"
            raise RuntimeError(error_msg)

        if self.Sort not in [n for n in RfcFieldName]:
            fields = ", ".join([f"'{n}'" for n in RfcFieldName])
            raise RuntimeError(f"Invalid sort field, valid fields include {fields}")

        if self.SortDir not in ["ASC", "DESC"]:
            raise RuntimeError("Sort direction must be 'ASC' or 'DESC'")
