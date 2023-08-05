'''Plugged provides an extremely lightweight set of utils around
importlib.machinery.SourceFileLoader for simplistic yet powerful importing.

.. include:: ../docs/howto.md
'''


import os.path

from . import entry, imp, mixin
from .entry import point

from types import SimpleNamespace
from typing import Iterable, Tuple, Any


Module = Any
Plugin = Tuple[str, Module]
Plugins = Iterable[Plugin]
Modules = Iterable[Module]


def im(glob: str) -> Any:
    '''Imports files from a glob path. If there are multiple files
    from the glob path this will return a namespace with all of them.
    Otherwise it returns a direct reference to a single module.'''
    plugins = list(load(glob))
    if len(plugins) == 1:
        name, module = plugins.pop(0)
        return module
    return namespace(plugins)


def load(glob: str) -> Plugins:
    '''Loads all of the files matched from a glob path.'''
    yield from imp.clean(imp.load(glob))


def modules(plugins: Plugins) -> Modules:
    '''Converts a list of Plugins to just modules, This simply removes the
    name field of the (name, module) pair.'''
    yield from (plug for (name, plug) in plugins)


def namespace(plugins: Plugins) -> SimpleNamespace:
    '''Converts a list of plugins to a namespace.'''
    return SimpleNamespace(**dict(plugins))


def points(glob: str) -> Plugins:
    '''Import files from a glob and returns just the points.'''
    for (name, module) in imp.load(glob):
        yield from entry.points(module)
