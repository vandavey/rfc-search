"""
Utility functions and types module.
"""
from alias import any_t, predicate_t, selector_t
from constants import URL_RGX


def select(values: list[any_t], func: selector_t) -> list[any_t]:
    """
    Project a list of values based using a projection functor.
    """
    return [*map(func, values)] if values else []


def where(values: list[any_t], func: predicate_t | None) -> list[any_t]:
    """
    Filter a list of values using a filter functor.
    """
    return [*filter(func, values)] if values else []


def valid_url(url: str) -> bool:
    """
    Determine whether the given URL is valid.
    """
    return bool(URL_RGX.match(url))
