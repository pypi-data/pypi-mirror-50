'''Mixin contains classes useful for creating subclass mixins.

.. include:: ../docs/entryextend.md
'''

import inspect
import functools

from . import entry, imp


class Extend:

    def __init__(self, plugins):
        self.__plugged__ = list(plugins)
        self.extend(self.__plugged__)

    def extend(self, points):
        for (name, point) in points:
            self.__dict__[name] = point
        return None


class PointExtend(Extend):

    def __init__(self, points):
        super().__init__(points)

    def extend(self, points):
        for (name, point) in points:
            if inspect.isclass(point.ref):
                attrs = ((x, getattr(point.ref, x)) for x in dir(point.ref))
                for (name, point) in ((x, y) for x, y in attrs if isinstance(y, entry.Point)):
                    self.__dict__[name] = functools.partial(point.ref, self)
            else:
                self.__dict__[name] = point.ref
