"""
Module for type alias definitions.
"""
from argparse import Namespace
from typing import Any, Callable, TypeAlias

# Command-line arguments type alias
args_t: TypeAlias = Namespace

# Unconstrained callable type alias
func_t: TypeAlias = Callable[..., Any]

# Module export symbols
__all__ = ["args_t", "func_t"]
