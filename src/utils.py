#
#  utils.py
#  --------
#  Module for miscellaneous utility functions and types.
#
import enum
import re


@enum.unique
class RfcFieldName(enum.StrEnum):
    """
    RFC metadata field name enumeration type.
    """
    ID: str = "Number"
    FILES: str = "Files"
    TITLE: str = "Title"
    AUTHORS: str = "Authors"
    DATE: str = "Date"
    MORE_INFO: str = "More Info"
    STATUS: str = "Status"


@enum.unique
class RfcFieldPos(enum.IntEnum):
    """
    RFC metadata field position enumeration type.
    """
    ID: int = 0
    FILES: int = 1
    TITLE: int = 2
    AUTHORS: int = 3
    DATE: int = 4
    MORE_INFO: int = 5
    STATUS: int = 6


def valid_url(url: str) -> bool:
    """
    Determine whether the given URL is valid.
    """
    patterns_parts = [
        r"?:[a-zA-Z]",
        r"[0-9]",
        r"[$-_@.&+]",
        r"[!*\(\),]",
        r"(?:%[0-9a-fA-F][0-9a-fA-F])"
    ]
    full_pattern = rf"(http|https)?://({'|'.join(patterns_parts)})+"

    return bool(re.match(full_pattern, url.strip()))
