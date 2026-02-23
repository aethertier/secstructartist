from __future__ import annotations
from pathlib import Path
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from typing import (
    Any, IO, List, Literal, Union, Tuple
)

__all__ = [
    'ColorType',
    'DrawnArtist',
    'LegendHandlesLabels',
    'ArtistKW',
    'PathOrFile',
    'FileFormat'
]

#
# --- Matplotlib-related types ---
#
ColorType = Any # e.g. '#1f76b4' or 'papayawhip'

DrawnArtist = Union[Line2D, Patch]

LegendHandlesLabels = Tuple[
    List[Tuple[DrawnArtist, ...]],  # List of legend handles
    List[str]                       # List of legend labels
]

#
# --- File IO-related types ---
#
ArtistKW = Literal[
    'default',
    'simple',
    'pymol',
    'pymol1',
    'pymol2',
    'pymol3',
    'dssp',
    'stride',
]

PathOrFile = Union[IO[str], Path, str]

FileFormat = Literal['yaml', 'json', 'auto']