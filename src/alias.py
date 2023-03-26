"""
Module for type alias definitions.
"""
from argparse import Namespace
from typing import Any, Callable, TypeAlias

# Any data type alias
any_t: TypeAlias = Any

# Command-line arguments type alias
args_t: TypeAlias = Namespace

# Unconstrained callable type alias
func_t: TypeAlias = Callable[..., any_t]

# void_t return type alias
void_t: TypeAlias = None

# Module export symbols
__all__ = ["any_t", "args_t", "func_t", "void_t"]
