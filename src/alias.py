"""
Type alias definitions module.
"""
from argparse import Namespace
from typing import Any, Callable, TypeAlias

# Any datatype type alias
any_t: TypeAlias = Any

# Command-line arguments type alias
args_t: TypeAlias = Namespace

# Unconstrained callable type alias
func_t: TypeAlias = Callable[..., any_t]

# Filter predicate function type alias
predicate_t: TypeAlias = Callable[[any_t], bool]

# Projection function type alias
selector_t: TypeAlias = Callable[[any_t], any_t]

# Void type alias
void_t: TypeAlias = None
