"""
Module for console utilities and control sequence processing.
"""
import enum
import os
import sys
import utils
from typing import TextIO
from alias import any_t, func_t, void_t

_ESC = "\033"
_RESET = f"{_ESC}[0m"


@enum.unique
class Color(enum.StrEnum):
    """
    Console color string enumeration type.
    """
    CYAN = f"{_ESC}[38;2;0;255;255m"
    RED = f"{_ESC}[38;2;246;0;0m"
    GREEN = f"{_ESC}[38;2;166;226;46m"
    YELLOW = f"{_ESC}[38;2;250;230;39m"


@enum.unique
class LevelSymbol(enum.StrEnum):
    """
    Console status level symbol enumeration type.
    """
    INFO = "[*]"
    ERROR = "[x]"
    VERBOSE = "[+]"
    WARN = "[!]"


class ExternError(RuntimeError):
    """
    External function runtime exception.
    """
    def __init__(self, extern: func_t, ecode: int) -> None:
        """
        Initialize the object.
        """
        self.Extern: func_t = extern
        self.ErrorCode: int = ecode

    def __repr__(self) -> str:
        """
        Get the string representation of the object.
        """
        return f"{self.__class__.__name__}({self.Extern}, {self.ErrorCode})"

    def __str__(self) -> str:
        """
        Get the user-readable string representation of the object.
        """
        return f"Extern <{self.Extern.__name__}> failed with error {self.ErrorCode}"


def _is_win_os() -> bool:
    """
    Determine whether the local operating system is Windows.
    """
    return os.name == "nt"


# Windows-specific imports, constants and globals
if _is_win_os():
    import ctypes
    from ctypes import c_long, c_ulong, c_void_p, WinDLL

    _ENABLE_PROCESSED_OUTPUT: int = 0x0001             # Enable ASCII sequences
    _ENABLE_VIRTUAL_TERMINAL_INPUT: int = 0x0200       # Enable input VT sequences
    _ENABLE_VIRTUAL_TERMINAL_PROCESSING: int = 0x0004  # Enable output VT sequences

    _INVALID_HANDLE_VALUE: int = -1  # Invalid handle value
    _STDIN_HANDLE_ID: int = -10      # Standard input buffer handle ID
    _STDOUT_HANDLE_ID: int = -11     # Standard output buffer handle ID

    _externs_setup: bool = False  # External function setup completed

    _kernel32: WinDLL = ctypes.windll.kernel32  # Windows 'kernel32' DLL

_vt_seq_enabled: bool = not _is_win_os()  # VT sequences processing enabled


def _assert_win_os(caller: func_t) -> void_t:
    """
    Raise a runtime error if the local system is not Windows.
    """
    if not _is_win_os():
        raise RuntimeError(f"<{caller.__name__}> is only supported on Windows")


def _assert_externs_setup() -> void_t:
    """
    Raise a runtime error if the Windows Console API
    external function are not configured.
    """
    _assert_win_os(_assert_externs_setup)

    if not _externs_setup:
        raise RuntimeError(f"Externs must be setup by calling <{_setup_externs}>")


def _assert_valid_handle(handle: int, caller: func_t) -> void_t:
    """
    Raise a runtime or value error if the given handle is invalid.
    """
    _assert_win_os(_assert_valid_handle)

    if handle == _INVALID_HANDLE_VALUE:
        raise ValueError(f"Invalid handle passed to <{caller.__name__}>: {handle}")


def _setup_externs() -> bool:
    """
    Configure all external Windows Console API functions.
    """
    _assert_win_os(_setup_externs)

    global _externs_setup, _kernel32

    if not _externs_setup:
        _kernel32.GetLastError.argtypes = []
        _kernel32.GetLastError.restype = c_long

        _kernel32.GetStdHandle.argtypes = [c_ulong]
        _kernel32.GetStdHandle.restype = c_void_p

        _kernel32.GetConsoleMode.argtypes = [c_void_p, ctypes.POINTER(c_ulong)]
        _kernel32.GetConsoleMode.restype = c_long

        _kernel32.SetConsoleMode.argtypes = [c_void_p, c_ulong]
        _kernel32.SetConsoleMode.restype = c_long

        _externs_setup = True

    return _externs_setup


def _get_last_error() -> int:
    """
    Get the calling thread's most recent error code using the Windows API.
    """
    _assert_win_os(_get_last_error)
    _assert_externs_setup()

    global _kernel32

    return int(_kernel32.GetLastError())


def _get_std_handle(buffer_hid: int) -> int:
    """
    Get a handle to the given standard console buffer handle
    ID using the Windows Console API.
    """
    _assert_win_os(_get_std_handle)
    _assert_externs_setup()

    global _kernel32

    if buffer_hid not in [_STDIN_HANDLE_ID, _STDOUT_HANDLE_ID]:
        raise ValueError(f"Invalid console buffer handle ID: {buffer_hid}")

    buffer_handle = _kernel32.GetStdHandle(buffer_hid)

    if buffer_handle == _INVALID_HANDLE_VALUE:
        raise ExternError(_kernel32.GetStdHandle, _get_last_error())

    return int(buffer_handle)


def _get_console_mode(std_handle: int) -> int:
    """
    Get the input or output mode of the console buffer corresponding to the
    given console input or output buffer handle using the Windows Console API.
    """
    _assert_win_os(_get_console_mode)
    _assert_externs_setup()
    _assert_valid_handle(std_handle, _get_console_mode)

    global _kernel32

    c_mode = c_ulong()

    if not _kernel32.GetConsoleMode(c_void_p(std_handle), ctypes.pointer(c_mode)):
        raise ExternError(_kernel32.GetConsoleMode, _get_last_error())

    return c_mode.value


def _set_console_mode(std_handle: int, mode: int) -> void_t:
    """
    Set the input or output mode of the console buffer corresponding to the given
    console input or output buffer handle using the Windows Console API.
    """
    global _kernel32

    _assert_win_os(_set_console_mode)
    _assert_externs_setup()
    _assert_valid_handle(std_handle, _set_console_mode)

    mode |= _get_console_mode(std_handle)

    if not _kernel32.SetConsoleMode(c_void_p(std_handle), c_ulong(mode)):
        raise ExternError(_kernel32.SetConsoleMode, _get_last_error())


def _enable_vt_seq() -> bool:
    """
    Enable virtual terminal sequence processing for the standard
    input and standard output console buffers.
    """
    _assert_win_os(_enable_vt_seq)

    global _vt_seq_enabled

    if not _vt_seq_enabled:
        if not _setup_externs():
            raise RuntimeError("Failed to configure external functions")

        stdin_mode = _ENABLE_VIRTUAL_TERMINAL_INPUT
        stdout_mode = _ENABLE_PROCESSED_OUTPUT | _ENABLE_VIRTUAL_TERMINAL_PROCESSING

        _set_console_mode(_get_std_handle(_STDIN_HANDLE_ID), stdin_mode)
        _set_console_mode(_get_std_handle(_STDOUT_HANDLE_ID), stdout_mode)

        _vt_seq_enabled = True

    return _vt_seq_enabled


def _console_title(title: str) -> void_t:
    """
    Set the title of the current console window.
    """
    if not _vt_seq_enabled:
        raise RuntimeError(f"Call <{_enable_vt_seq}> to enable VT control sequences")

    print(f"{_ESC}]0;{title}\x07", end="")


def setup_console() -> void_t:
    """
    Customize the console title and enable virtual terminal processing.
    """
    if _is_win_os() and not _enable_vt_seq():
        raise RuntimeError("Error occurred enabling virtual terminal processing")

    _console_title(utils.app_title())


def write_ln(obj: any_t,
             color: Color = Color.CYAN,
             symbol: LevelSymbol = LevelSymbol.INFO,
             stream: TextIO = sys.stdout) -> void_t:
    """
    Write a line prefixed with a colored status level
    symbol to the specified output console stream.
    """
    print(f"{color}{symbol}{_RESET} {obj}{_RESET}", file=stream)


def error_ln(obj: any_t) -> void_t:
    """
    Write an error line to the standard error console stream.
    """
    write_ln(obj, color=Color.RED, symbol=LevelSymbol.ERROR, stream=sys.stderr)


def warn_ln(obj: any_t) -> void_t:
    """
    Write a warning line to the standard error console stream.
    """
    write_ln(obj, color=Color.YELLOW, symbol=LevelSymbol.WARN, stream=sys.stderr)


# Module export symbols
__all__ = ["Color", "LevelSymbol", "ExternError"]
