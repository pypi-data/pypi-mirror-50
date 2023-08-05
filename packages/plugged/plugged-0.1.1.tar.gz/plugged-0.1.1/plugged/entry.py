'''Provides entry point decorators and checkers for creating easy to find functions.

An entry point is just a Point wrapper with the original reference in a var.
Making these entry points nothing more than slight decoration.
'''


import inspect
import glob

from functools import wraps


class Point:

    def __init__(self, ref):
        self.ref = ref

    def __call__(self, *args, **kwargs):
        return self.ref(*args, **kwargs)


def points(module):
    items = ((name, getattr(module, name)) for name in dir(module))
    yield from ((name, point) for (name, point) in items if isinstance(point, Point))


def point(point):
    wrap = wraps(point)
    def run(*args, **kwargs):
        return point(*args, **kwargs)
    return wrap(Point(point))
