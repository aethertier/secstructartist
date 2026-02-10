from __future__ import annotations
from typing import Dict
from dataclasses import dataclass, asdict, replace


@dataclass(frozen=True)
class DrawStyle:
    """Global settings for a secondary structure drawing"""
    height: float = 1.
    stride: float = 1.
    linewidth: float = 1.
    zorder: float = 5.

    def with_updates(self, **changes) -> DrawStyle:
        return replace(self, **changes)
    
    def to_dict(self) -> Dict[str, float]:
        return asdict(self)