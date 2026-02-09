from __future__ import annotations
from hashlib import blake2s
from typing import Any, Dict, Optional, TYPE_CHECKING
from .utils_ import write_configuration

if TYPE_CHECKING:
    from ..secstructartist import SecStructArtist
    from ..elementartist import ElementArtist
    from ..primitives import PrimitiveArtist
    from ..typing_ import PathOrFile, FileFormat


class SSAConfigWriter:

    def __init__(self, artist: Optional[SecStructArtist] = None):
        self._drawstyle: Dict[str, float] = {}
        self._elements: Dict[str, Dict[str, Any]] = {}
        self._primitives_ids: Dict[int, str] = {}
        self._primitives: Dict[str, Dict[str, Any]] = {}
        if artist:
            self.register_secstructartist(artist)

    def register_elementartist(self, element: ElementArtist, element_key: str) -> str:
        """Register an ElementArtist"""
        if element_key in self._elements:
            raise ValueError((
                f"An ElementArtist with key '{element_key}' is already registered. "
                "Forgot to run `.reset()` ?"
            ))
        self._elements[element_key] = {
            'label': element.label,
            'primitives': [self.register_primitiveartist(prim) for prim in element.primitives]
        }
        return element_key

    def register_primitiveartist(self, primitive: PrimitiveArtist) -> str:
        """Register a PrimitiveAritst"""
        primitive_key = self._register_primitiveartist_key(primitive)
        self._primitives[primitive_key] = primitive.to_dict()
        return primitive_key

    def register_secstructartist(self, artist: SecStructArtist):
        """Register a complete SecStructArtist"""
        for elem_key, elem_artist in artist.elements.items():
            self.register_elementartist(elem_artist, element_key=elem_key)
        self._drawstyle = artist.drawstyle.to_dict()
        
    def reset(self):
        """Resets the whole registry"""
        self._drawstyle = {}
        self._elements = {}
        self._primitives_ids = {}
        self._primitives = {}

    def get_dict(self):
        return {
            'drawstyle': self._drawstyle,
            'elements': self._elements, 
            'primitives': self._primitives,
        }

    def write(self, file_: PathOrFile, format_: FileFormat='auto', **kwargs):
        data = self.get_dict()
        return write_configuration(data, file_, format_, **kwargs)

    def _register_primitiveartist_key(self, primitive: PrimitiveArtist) -> str:
        """Registers and returns a unique identifier for a PrimitiveArtist"""
        prim_id = id(primitive)
        if prim_id in self._primitives_ids:
            return self._primitives_ids[prim_id]
        prim_type = type(primitive).__name__
        hashed_id = blake2s(prim_id.to_bytes(8, 'big'), digest_size=3)
        x = int.from_bytes(hashed_id.digest(), 'big')
        # Avoid id clashes, but limit iterations to prevent infinite loops (extremely unlikely!)
        for _ in range(100):
            prim_key = f'{prim_type}-{x:06x}'
            if prim_key not in self._primitives:
                break
            x += 1
            x %= 0x1000000
        else:
            raise RuntimeError(f'Unable to generate key for primitve: {primitive!r}')
        self._primitives_ids[prim_id] = prim_key
        return prim_key