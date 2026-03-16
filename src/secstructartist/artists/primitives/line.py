from __future__ import annotations
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from .base import PrimitiveArtist, DrawContext


class LinePrimitive(PrimitiveArtist):
    """
    Draws a straight line. This primitive typically represents random coil or loops.
    """
    def __init__(self, *, zorder_offset: float = -.1, **kwargs):
        super().__init__(zorder_offset=zorder_offset, **kwargs)

    @staticmethod
    def _draw(ctx: DrawContext, ax: Axes) -> Line2D:
        line = Line2D(
            [ctx.x_left, ctx.x_right], [ctx.y_center, ctx.y_center],
            linewidth=ctx.linewidth,
            color=ctx.linecolor,
            zorder=ctx.zorder,
            solid_capstyle="butt"
        )
        ax.add_line(line)
        ax.update_datalim(line.get_xydata())
        return line
    
    @staticmethod
    def _get_legend_handle(ctx: DrawContext) -> Line2D:
        line = Line2D([ctx.x_left, ctx.x_right], [ctx.y_center, ctx.y_center],
            linewidth=ctx.linewidth,
            color=ctx.linecolor,
        )
        return line