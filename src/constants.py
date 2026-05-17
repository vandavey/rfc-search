"""
Constant definitions definitions module.
"""
import os
import re
from re import Pattern

# Application source code repository URL
_REPO_URL: str = "https://github.com/vandavey/rfc-search"

# HTML anchor tag
A_TAG: str = "a"

# Application name
APP_NAME: str = "rfc-search.py"

# Application title
APP_TITLE: str = f"{APP_NAME} ({_REPO_URL})"

# HTML division tag
DIV_TAG: str = "div"

# ANSI escape control sequence
ESC: str = "\033"

# HTML hypertext reference attribute
HREF_ATTR: str = "href"

# HTML list item tag
LI_TAG: str = "li"

# ANSI reset control sequence
RESET: str = f"{ESC}[0m"

# RFC search URI
SEARCH_URI: str = "https://www.rfc-editor.org/search/rfc_search_detail.php"

# HTML table tag
TABLE_TAG: str = "table"

# HTML table data tag
TD_TAG: str = "td"

# HTML table header tag
TH_TAG: str = "th"

# HTML table row tag
TR_TAG: str = "tr"

# URL regular expression
URL_RGX: Pattern[str] = re.compile(
    r"http(s)?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|%[0-9a-fA-F][0-9a-fA-F])"
)

# Current operating system is Windows
USING_WIN_OS: bool = os.name == "nt"

if USING_WIN_OS:
    # Enable ANSI control sequences
    ENABLE_PROCESSED_OUTPUT: int = 0x0001

    # Enable input virtual terminal sequences
    ENABLE_VIRTUAL_TERMINAL_INPUT: int = 0x0200

    # Enable output virtual terminal sequences
    ENABLE_VIRTUAL_TERMINAL_PROCESSING: int = 0x0004

    # Invalid handle value
    INVALID_HANDLE_VALUE: int = -1

    # Standard input buffer handle ID
    STDIN_HANDLE_ID: int = -10

    # Standard output buffer handle ID
    STDOUT_HANDLE_ID: int = -11
