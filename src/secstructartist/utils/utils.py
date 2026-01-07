from dataclasses import dataclass, field
from importlib import metadata
from typing import Iterable

try:
    __version__ = metadata.version("secstructartist")
except metadata.PackageNotFoundError:
    __version__ = "NOT INSTALLED"


@dataclass(repr=False)
class DrawnSecStructElement:
    """Return object for all element artists that allows 
    access to the secondary"""
    element_type: str = None
    start: float = None
    stop: float = None
    lines: list = field(default_factory=list)
    # collections: list = field(default_factory=list)
    patches: list = field(default_factory=list)

    def __repr__(self):
        return "Drawn{0}(start:{1}, stop:{2}, lines:{3}, patches:{4})".format(
            self.element_type, self.start, self.stop, len(self.lines), len(self.patches))
    

def iterate_blocks(primary: Iterable, *secondary: Iterable):
    prv = primary[0]
    i = 0
    for j, cur in enumerate(primary):
        if cur != prv:
            yield (prv, *[s[i:j] for s in secondary])
            prv, i = cur, j
    j += 1
    yield (prv, *[s[i:j] for s in secondary])