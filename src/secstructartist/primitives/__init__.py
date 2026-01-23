from .base import PrimitiveArtist
from .arrow import ArrowPrimitive
from .helix import HelixPrimitive
from .line import LinePrimitive

PRIMITIVES_AVAIL = {
    'ArrowPrimitive': ArrowPrimitive,
    'HelixPrimitive': HelixPrimitive,
    'LinePrimitive': LinePrimitive,
}