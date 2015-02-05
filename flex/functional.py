import operator
import functools

from flex.constants import EMPTY


def chain_reduce(value, functions, **kwargs):
    for function in functions:
        value = function(value, **kwargs)
    return value


def chain_reduce_partial(*functions):
    """
    Given an iterable of functions, returns a callable that takes a value and
    passes it through all of the given functions in order.

    def a(x):
        ...

    def b(x):
        ...

    c = chain_reduce_partial(a, b)

    This is equivilent to

    def c(x):
        return b(a(x))
    """
    return functools.partial(
        chain_reduce,
        functions=functions,
    )


def apply_functions_to_key(key, *funcs):
    """
    Shortcut for the common pattern with `chain_reduce_partial` for applying a
    validator to some specified key in a mapping.
    """
    return chain_reduce_partial(
        operator.methodcaller('get', key, EMPTY), *funcs
    )
