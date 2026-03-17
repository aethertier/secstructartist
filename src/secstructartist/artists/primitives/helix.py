from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, Union
from matplotlib.axes import Axes
from matplotlib.patches import PathPatch, Rectangle

from .base import PrimitiveArtist, DrawContext
from ._helpers.helixpath import HelixPathHelper
from ..drawstyle import DrawStyle


@dataclass(slots=True)
class HelixContext(DrawContext):
    num_halfturns: int
    dx_halfturn: float
    dx_ribbon: float
    fill_inner_ribbon: bool


class HelixPrimitive(PrimitiveArtist):
    """
    Draws a wound ribbon. This primitive typically represents helices.

    The wound ribbon is generated as a PathPatch, and the *inside* can be made 
    transparent allowing for color differences of the *inside* and *outside* helix.
    """

    def __init__(
        self,
        *,
        ribbon_width: Union[float, None] = None,
        ribbon_period: float = 3.6,
        fill_inner_ribbon: bool = True,
        **kwargs,
    ):
        """
        Parameters
        ----------

        ribbon_width: float or None
            The width of the ribbon representing the helix in units of ``DrawStyle.stride``.
            If ``None``, it is set to ``0.5 * ribbon_period``

        ribbon_period: 
            Controls the number of turns in a helix element. The number of turns
            for a given element is calculated as the length of the element 
            devided by the ```ribbon_period`` rounded to half-turns.


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
        self.ribbon_width = ribbon_width
        self.ribbon_period = ribbon_period
        self.fill_inner_ribbon = fill_inner_ribbon

    def resolve_drawstyle(self, drawstyle: DrawStyle, x: float=1, y: float=1, length: int=1) -> HelixContext:
        """Create a drawing context from a drawstyle as prequisite for rendering"""
        num_halfturns = int(max(1, round(2 * length / self.ribbon_period)))
        dx_ribbon = (.5 * self.ribbon_period * drawstyle.stride) if self.ribbon_width is None else \
            (self.ribbon_width * drawstyle.stride)
        ctxdict = asdict(super().resolve_drawstyle(drawstyle, x, y, length))
        ctxdict.update(dict(
            num_halfturns = num_halfturns,
            dx_halfturn = ctxdict['dx'] / float(num_halfturns),
            dx_ribbon = dx_ribbon,
            fill_inner_ribbon = self.fill_inner_ribbon,
        ))
        return HelixContext(**ctxdict)

    @staticmethod
    def _draw(ctx: HelixContext, ax: Axes) -> PathPatch:
        path = HelixPathHelper.make_path(ctx)
        helix = PathPatch(
            path,
            linewidth = ctx.linewidth,
            facecolor = ctx.fillcolor,
            edgecolor = ctx.linecolor,
            alpha = ctx.alpha,
            zorder = ctx.zorder
        )
        ax.add_patch(helix)
        ax.update_datalim(path.vertices)
        return helix
        
    @staticmethod
    def _get_legend_handle(ctx: HelixContext) -> Rectangle:
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
            ribbon_width = self.ribbon_width,
            ribbon_period = self.ribbon_period,
            fill_inner_ribbon = self.fill_inner_ribbon,
        ))
        return outdict
