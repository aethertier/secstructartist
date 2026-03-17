from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict
from matplotlib.axes import Axes
from matplotlib.patches import Polygon, Rectangle
from .base import PrimitiveArtist, DrawContext
from ..drawstyle import DrawStyle


@dataclass(slots=True)
class ArrowContext(DrawContext):
    dx_tip: float
    dy_tip: float
    dy_shaft: float


class ArrowPrimitive(PrimitiveArtist):
    """
    Draws an arrow-shape. This primitive typically represents beta strands.

    The arrow-shape is generated as a polygon an can be filled. If the length
    of the element is too short, only the arrow tip without a shaft is drawn.
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
            Length of the arrow tip in units of ``drawstyle.stride``.

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
        self.height_scalar2 = height_scalar2

    def resolve_drawstyle(self, drawstyle: DrawStyle, x: float=1, y: float=1, length: int=1) -> ArrowContext:
        """Create a drawing context from a drawstyle as prequisite for rendering"""
        ctxdict = asdict(super().resolve_drawstyle(drawstyle, x, y, length))
        dy_shaft = (.7 * ctxdict['dy']) if self.height_scalar2 is None else \
            (.5 * drawstyle.height * self.height_scalar2)
        ctxdict.update(dict(
            dy_tip = ctxdict['dy'],
            dy_shaft = dy_shaft,
            dx_tip = self.arrow_tip_length * drawstyle.stride
        ))
        return ArrowContext(**ctxdict)

    @staticmethod
    def _draw(ctx: ArrowContext, ax: Axes) -> Polygon:
        tip_y0, tip_y1 = ctx.y - ctx.dy_tip, ctx.y + ctx.dy_tip
        shaft_y0, shaft_y1 = ctx.y - ctx.dy_shaft, ctx.y + ctx.dy_shaft
        x0  = ctx.x # Left position: arrow-shaft start
        x1 = ctx.x + ctx.dx  # Right position: arrow-point
        x_tip = x1 - ctx.dx_tip # Tip position: tip start

        # Case: Draw arrow without shaft
        if x_tip <= x0:
            xypath = [
                [x0, tip_y1],
                [x1, ctx.y],
                [x0, tip_y0],
            ]
        else:
            # Case: Path for arrow without shaft
            xypath = [
                [x0, shaft_y1],
                [x_tip, shaft_y1],
                [x_tip, tip_y1],
                [x1, ctx.y],
                [x_tip, tip_y0],
                [x_tip, shaft_y0],
                [x0, shaft_y0],
            ]

        sheet = Polygon(xypath, closed=True,
            linewidth = ctx.linewidth,
            edgecolor = ctx.linecolor,
            facecolor = ctx.fillcolor,
            alpha = ctx.alpha,
            zorder = ctx.zorder,
        )
        ax.add_patch(sheet)
        ax.update_datalim(sheet.get_xy())
        return sheet

    @staticmethod
    def _get_legend_handle(ctx: ArrowContext) -> Rectangle:
        """Returns a handle for a legend, currently just a rectangle"""
        rec = Rectangle(
            (0.,0.), width=1., height=1.,
            linewidth = ctx.linewidth,
            edgecolor = ctx.linecolor,
            facecolor = ctx.fillcolor,
            alpha = ctx.alpha,
        )
        return rec

    def to_dict(self) -> Dict[str, Any]:
        """Returns a serializeable dictionary capturing all attributes of the primitive"""
        outdict = super().to_dict()
        outdict.update(dict(
            arrow_tip_length = self.arrow_tip_length,
            height_scalar2 = self.height_scalar2
        ))
        return outdict
