from __future__ import annotations
from typing import  TYPE_CHECKING
from matplotlib.lines import Line2D
from .base import PrimitiveArtist

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from ..core.drawstyle import DrawStyle


class LinePrimitive(PrimitiveArtist):

    def draw(self, x: float, y: float, length: int, ax: Axes, drawstyle: DrawStyle) -> Line2D:
        x0, y0 = x + self.x_offset, y + self.y_offset
        x1 = x0 + drawstyle.step * length
        line = Line2D(
            [x0, x1], [y0, y0], 
            linewidth=drawstyle.linewidth * self.linewidth_scalar,
            color=self.linecolor,
            zorder=drawstyle.zorder - .1 + self.zorder_offset
        )
        ax.add_line(line)
        ax.update_datalim(line.get_xydata())
        ax.autoscale_view()
        return line

    def get_legend_handle(self, drawstyle: DrawStyle) -> Line2D:
        line = Line2D([0.0, 1.0], [0.5, 0.5],
            linewidth=drawstyle.linewidth * self.linewidth_scalar,
            color=self.linecolor,
        )
        return line