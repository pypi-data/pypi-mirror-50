import os.path
import importlib
import glob


def path(path: str, name: str=None):
    """Import a single path, optionally forcing the name."""
    name = name or os.path.basename(path)
    loader = importlib.machinery.SourceFileLoader(name, path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def load(globpath):
    files = glob.iglob(globpath)
    yield from ((filepath, path(filepath)) for filepath in files)


def clean(plugins):
    yield from ((_clean_path(path), module) for (path, module) in plugins)


def _clean_path(filepath):
    head, tail = os.path.split(filepath)
    name, ext = os.path.splitext(tail)
    return name
