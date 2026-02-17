from __future__ import annotations
from typing import Any, Dict, TYPE_CHECKING
from matplotlib.lines import Line2D
from .base import PrimitiveArtist

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from ..drawstyle import DrawStyle


class LinePrimitive(PrimitiveArtist):
    """
    Line primitive used for drawing linear secondary structure elements.

    This primitive draws a horizontal line segment whose length is determined
    by the number of residues in the element.
    """
    def __init__(self, *, zorder_offset: float = -.1, **kwargs):
        super().__init__(zorder_offset=zorder_offset, **kwargs)

    def draw(self, x: float, y: float, length: int, ax: Axes, drawstyle: DrawStyle) -> Line2D:
        x0, y0 = x + self.x_offset, y + self.y_offset
        x1 = x0 + drawstyle.stride * length
        line = Line2D(
            [x0, x1], [y0, y0], 
            linewidth=drawstyle.linewidth * self.linewidth_scalar,
            color=self.linecolor,
            zorder=drawstyle.zorder + self.zorder_offset
        )
        ax.add_line(line)
        ax.update_datalim(line.get_xydata())
        return line

    def get_legend_handle(self, drawstyle: DrawStyle) -> Line2D:
        line = Line2D([0.0, 1.0], [0.5, 0.5],
            linewidth=drawstyle.linewidth * self.linewidth_scalar,
            color=self.linecolor,
        )
        return line

    def to_dict(self) -> Dict[str, Any]:
        return super().to_dict()