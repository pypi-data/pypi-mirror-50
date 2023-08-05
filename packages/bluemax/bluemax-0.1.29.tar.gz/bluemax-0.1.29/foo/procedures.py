""" an example function and exposing it through __all__ """

__all__ = ['add']


def add(int_a: int, int_b: int) -> int:
    """ simple addition of two integers"""
    return int_a + int_b
