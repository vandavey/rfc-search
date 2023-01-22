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
    ID = "Number"
    FILES = "Files"
    TITLE = "Title"
    AUTHORS = "Authors"
    DATE = "Date"
    MORE_INFO = "More Info"
    STATUS = "Status"


@enum.unique
class RfcFieldPos(enum.IntEnum):
    """
    RFC metadata field position enumeration type.
    """
    ID = 0
    FILES = 1
    TITLE = 2
    AUTHORS = 3
    DATE = 4
    MORE_INFO = 5
    STATUS = 6


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
