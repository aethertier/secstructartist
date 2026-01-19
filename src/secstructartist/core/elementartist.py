from __future__ import annotations
from typing import Sequence, TYPE_CHECKING
from ..primitives.base import PrimitiveArtist


if TYPE_CHECKING:
    from .drawstyle import DrawStyle



class ElementArtist:

    def __init__(self, primitives: Sequence[PrimitiveArtist], label: str=''):
        self.primitives = primitives
        self.label = label

    def draw(self, x, y, ax, drawstyle):
        pass

    def legend_handle(self, drawstyle):
        pass
