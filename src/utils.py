"""
Module for miscellaneous utility functions and types.
"""
import enum
import re
from enum import IntEnum, StrEnum


@enum.unique
class MetaField(IntEnum):
    """
    RFC specification metadata field integral enumeration type.
    """
    ID = 0
    FILES = 1
    TITLE = 2
    AUTHORS = 3
    DATE = 4
    MORE_INFO = 5
    STATUS = 6


@enum.unique
class MetaFieldName(StrEnum):
    """
    RFC specification metadata field name string enumeration type.
    """
    ID = "Number"
    FILES = "Files"
    TITLE = "Title"
    AUTHORS = "Authors"
    DATE = "Date"
    MORE_INFO = "More Info"
    STATUS = "Status"


def repo_url() -> str:
    """
    Get the application source code repository URL.
    """
    return "https://github.com/vandavey/rfc-search"


def app_name() -> str:
    """
    Get the rfc-search application name.
    """
    return "rfc-search.py"


def app_title() -> str:
    """
    Get the rfc-search application title.
    """
    return f"{app_name()} ({repo_url()})"


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


# Module export symbols
__all__ = ["MetaFieldName", "MetaField"]
