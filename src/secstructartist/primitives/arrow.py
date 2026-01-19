from __future__ import annotations
from typing import TYPE_CHECKING
from matplotlib.patches import Polygon
from .base import PrimitiveArtist

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from ..core.drawstyle import DrawStyle

class ArrowPrimitive(PrimitiveArtist):
    """
    Arrow-shaped primitive used to represent beta strands.

    This primitive draws a filled polygon in the shape of an arrow, with an
    optional shaft and configurable arrow tip length.
    """

    def __init__(
        self,
        *,
        arrow_tip_length: float = 3.,
        height_scalar2: float = None,
        **kwargs,
    ):
        """
        Parameters
        ----------
        arrow_tip_length : float, default=3.0
            Length of the arrow tip in units of ``drawstyle.step``.

        height_scalar2 : float, optional
            Height of the arrow shaft relative to the element height. If None,
            it defaults to ``0.7 * height_scalar``.

        Other Parameters
        ----------------
        xy_offset : tuple of float
        height_scalar : float
        linewidth_scalar : float
        zorder_offset : float
        linecolor : ColorType
        fillcolor : ColorType or None
            See :class:`PrimitiveArtist`.
        """
        super().__init__(**kwargs)
        self.arrow_tip_length = arrow_tip_length
        self.height_scalar2 = height_scalar2 if height_scalar2 is not None else self.height_scalar * .7

    def draw(self, x: float, y: float, length: int, ax: Axes, drawstyle: DrawStyle) -> Polygon:
        x0, y2 = x + self.x_offset, y + self.y_offset
        x2 = x0 + drawstyle.step * length
        x1 = x2 - self.arrow_tip_length * drawstyle.step
        y0 = y2 - .5 * drawstyle.height * self.height_scalar
        y1 = y2 - .5 * drawstyle.height * self.height_scalar2
        y3 = y2 + .5 * drawstyle.height * self.height_scalar2
        y4 = y2 + .5 * drawstyle.height * self.height_scalar
        
        if x1 < x0:
            # Case: Draw arrow without shaft
            xypath = [
                [x0, y0],
                [x2, y2],
                [x0, y4],
            ]
        else:
            # Case: Path for arrow without shaft
            xypath = [
                [x0, y1],
                [x1, y1],
                [x1, y0],
                [x2, y2],
                [x1, y4],
                [x1, y3],
                [x0, y3],
            ]

        sheet = Polygon(xypath, closed=True, 
            linewidth = drawstyle.linewidth * self.linewidth_scalar,
            fill = (self.fillcolor is not None),
            edgecolor = self.linecolor, 
            facecolor = self.fillcolor,
            zorder = drawstyle.zorder + self.zorder_offset
        )
        ax.add_patch(sheet)
        return sheet

    def get_legend_handle(self, drawstyle: DrawStyle) -> Polygon:
        # Define a small, normalized arrow in legend coordinates
        # Legend handles typically live in a ~1x1 box
        xypath = [
            (0.0, 0.3),
            (0.6, 0.3),
            (0.6, 0.1),
            (1.0, 0.5),
            (0.6, 0.9),
            (0.6, 0.7),
            (0.0, 0.7),
        ]
        sheet = Polygon(xypath, closed=True, 
            linewidth = drawstyle.linewidth * self.linewidth_scalar,
            fill = (self.fillcolor is not None),
            edgecolor = self.linecolor, 
            facecolor = self.fillcolor,
        )
        return sheet