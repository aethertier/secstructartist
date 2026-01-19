from __future__ import annotations
from dataclasses import dataclass, replace


@dataclass(frozen=True, slots=True)
class DrawStyle:
    """Global settings for a secondary structure drawing"""
    height: float = 1.
    step: float = 1.
    linewidth: float = 1.
    zorder: float = 9.

    def with_updates(self, **changes) -> DrawStyle:
        return replace(self, **changes)