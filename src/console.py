"""
Console and control sequence processing module.
"""
from alias import any_t, func_t, void_t
from constants import (
    APP_TITLE,
    ESC,
    RESET,
    ENABLE_PROCESSED_OUTPUT,
    ENABLE_VIRTUAL_TERMINAL_INPUT,
    ENABLE_VIRTUAL_TERMINAL_PROCESSING,
    INVALID_HANDLE_VALUE,
    STDIN_HANDLE_ID,
    STDOUT_HANDLE_ID,
    USING_WIN_OS
)
from ctypes import c_long, c_ulong, c_void_p, POINTER, pointer
from enum import StrEnum, unique
from io import TextIOWrapper
from sys import stderr, stdout
from typing import TextIO

if USING_WIN_OS:
    from ctypes import WinDLL, windll

    _externs_setup: bool = False          # External function setup completed
    _kernel32: WinDLL = windll.kernel32   # Windows 'kernel32' DLL

_vt_seq_enabled: bool = not USING_WIN_OS  # VT sequences processing enabled


@unique
class Color(StrEnum):
    """
    Console color string enumeration.
    """
    CYAN = f"{ESC}[38;2;0;255;255m"
    RED = f"{ESC}[38;2;246;0;0m"
    GREEN = f"{ESC}[38;2;166;226;46m"
    YELLOW = f"{ESC}[38;2;250;230;39m"


@unique
class LogLevel(StrEnum):
    """
    Console status level symbol enumeration.
    """
    INFO = "[*]"
    ERROR = "[x]"
    VERBOSE = "[+]"
    WARN = "[!]"


class ExternError(RuntimeError):
    """
    External function runtime exception.
    """
    def __init__(self, extern: func_t, ecode: int) -> void_t:
        """
        Initialize the object.
        """
        self.Extern: func_t = extern
        self.ErrorCode: int = ecode

    def __repr__(self) -> str:
        """
        Developer-friendly string representation of the object.
        """
        return f"{self.__class__.__name__}({self.Extern}, {self.ErrorCode})"

    def __str__(self) -> str:
        """
        User-friendly string representation of the object.
        """
        return f"Extern <{self.Extern.__name__}> failed with error {self.ErrorCode}"


def _assert_win_os(caller: func_t) -> void_t:
    """
    Raise a runtime error if the local system is not Windows.
    """
    if not USING_WIN_OS:
        raise RuntimeError(f"<{caller.__name__}> is only supported on Windows.")


def _assert_externs_setup() -> void_t:
    """
    Raise a runtime error if the Windows Console API
    external function are not configured.
    """
    _assert_win_os(_assert_externs_setup)

    if not __debug__ and not _externs_setup:
        raise RuntimeError(f"Externs must be setup by calling <{_setup_externs}>.")


def _assert_valid_handle(handle: int, caller: func_t) -> void_t:
    """
    Raise a runtime or value error if the given handle is invalid.
    """
    _assert_win_os(_assert_valid_handle)

    if handle == INVALID_HANDLE_VALUE:
        raise ValueError(f"Invalid handle passed to <{caller.__name__}>: {handle}.")


def _setup_externs() -> bool:
    """
    Configure all external Windows Console API functions.
    """
    global _externs_setup, _kernel32
    _assert_win_os(_setup_externs)

    if not __debug__ and not _externs_setup:
        _kernel32.GetLastError.argtypes = []
        _kernel32.GetLastError.restype = c_long

        _kernel32.GetStdHandle.argtypes = [c_ulong]
        _kernel32.GetStdHandle.restype = c_void_p

        _kernel32.GetConsoleMode.argtypes = [c_void_p, POINTER(c_ulong)]
        _kernel32.GetConsoleMode.restype = c_long

        _kernel32.SetConsoleMode.argtypes = [c_void_p, c_ulong]
        _kernel32.SetConsoleMode.restype = c_long

        _externs_setup = True

    return _externs_setup


def _get_last_error() -> int:
    """
    Get the most recent error code of the calling thread via the Windows API.
    """
    global _kernel32

    _assert_win_os(_get_last_error)
    _assert_externs_setup()

    return int(_kernel32.GetLastError())


def _get_std_handle(buffer_hid: int) -> int:
    """
    Get a handle to the given standard console buffer handle
    ID using the Windows Console API.
    """
    global _kernel32

    _assert_win_os(_get_std_handle)
    _assert_externs_setup()

    if buffer_hid not in (STDIN_HANDLE_ID, STDOUT_HANDLE_ID):
        raise ValueError(f"Invalid console buffer handle ID: {buffer_hid}.")

    buffer_handle = _kernel32.GetStdHandle(buffer_hid)

    if buffer_handle == INVALID_HANDLE_VALUE:
        raise ExternError(_kernel32.GetStdHandle, _get_last_error())

    return int(buffer_handle)


def _get_console_mode(std_handle: int) -> int:
    """
    Get the input or output mode of the console buffer corresponding to the
    given console input or output buffer handle using the Windows Console API.
    """
    global _kernel32

    _assert_win_os(_get_console_mode)
    _assert_externs_setup()
    _assert_valid_handle(std_handle, _get_console_mode)

    c_mode = c_ulong()

    if not _kernel32.GetConsoleMode(c_void_p(std_handle), pointer(c_mode)):
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
            raise RuntimeError("Failed to configure external functions.")

        stdin_mode = ENABLE_VIRTUAL_TERMINAL_INPUT
        stdout_mode = ENABLE_PROCESSED_OUTPUT | ENABLE_VIRTUAL_TERMINAL_PROCESSING

        _set_console_mode(_get_std_handle(STDIN_HANDLE_ID), stdin_mode)
        _set_console_mode(_get_std_handle(STDOUT_HANDLE_ID), stdout_mode)

        _vt_seq_enabled = True

    return _vt_seq_enabled


def _console_title(title: str) -> void_t:
    """
    Set the title of the current console window.
    """
    if not __debug__ and not _vt_seq_enabled:
        raise RuntimeError(f"Call <{_enable_vt_seq}> to enable VT control sequences.")

    print(f"{ESC}]0;{title}\x07", end="")


def setup_console() -> void_t:
    """
    Customize the console title and enable virtual terminal processing.
    """
    if not __debug__ and USING_WIN_OS and not _enable_vt_seq():
        raise RuntimeError("Error occurred enabling virtual terminal processing.")

    _console_title(APP_TITLE)


def write_ln(
    obj: any_t,
    color: Color = Color.CYAN,
    log_level: LogLevel = LogLevel.INFO,
    stream: TextIO | TextIOWrapper = stdout
) -> void_t:
    """
    Write a line prefixed with a colored status level
    symbol to the specified output console stream.
    """
    print(f"{color}{log_level}{RESET} {obj}{RESET}", file=stream)


def error_ln(obj: any_t) -> void_t:
    """
    Write an error line to the standard error console stream.
    """
    write_ln(obj, color=Color.RED, log_level=LogLevel.ERROR, stream=stderr)


def warn_ln(obj: any_t) -> void_t:
    """
    Write a warning line to the standard error console stream.
    """
    write_ln(obj, color=Color.YELLOW, log_level=LogLevel.WARN, stream=stderr)
