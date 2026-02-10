from __future__ import annotations
from typing import Any, Dict, List, Tuple, Union, TYPE_CHECKING
import numpy as np
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path
from .base import PrimitiveArtist
from ._helpers.lineq import intersection

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from ..drawstyle import DrawStyle

Vertices = List[Tuple[float, float]]


class HelixPrimitive(PrimitiveArtist):
    """
    Arrow-shaped primitive used to represent beta strands.

    This primitive draws a filled polygon in the shape of an arrow, with an
    optional shaft and configurable arrow tip length.
    """

    def __init__(
        self,
        *,
        ribbon_width: Union[float, None] = None,
        ribbon_period: float = 3.6,
        fill_inner_ribbon: bool = False,
        **kwargs,
    ):
        """
        Parameters
        ----------

        ribbon_width: float or None
            The width of the ribbon representing the helix in units of ``DrawStyle.step``.
            If ``None``, it is set to ``0.3 * ribbon_period``

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

    @property
    def ribbon_width(self) -> float:
        if self._ribbon_width is None:
            return .6 * self.ribbon_period
        return self._ribbon_width
    
    @ribbon_width.setter
    def ribbon_width(self, value: float):
        self._ribbon_width = value

    def draw(self, x: float, y: float, length: int, ax: Axes, drawstyle: DrawStyle) -> PathPatch:
        # Num of halfturns
        num_halfturns = int(max(1, round(2 * length / self.ribbon_period)))
        dx = drawstyle.step * length / num_halfturns 
        dy = drawstyle.height * self.height_scalar * .5
        
        # Generate paths for consecutive turns
        vertices, downturn_new = [], [[x, y]]
        x_ = x
        for k in range(0, num_halfturns, 2):
            is_last = (num_halfturns - k) < 2
            downturn_prv = downturn_new
            downturn_new = self._pathgen_downturn(x_ + .5 * dx, y, dx, dy, last=is_last)
            upturn = self._pathgen_upturn(left=downturn_prv, right=downturn_new)
            vertices.append(upturn)
            vertices.append(downturn_new)
            x_ += 2 * dx
        if num_halfturns % 2 == 0:
            downturn_prv, downturn_new = downturn_new, [[x_, y]]
            upturn = self._pathgen_upturn(left=downturn_prv, right=downturn_new)
            vertices.append(upturn)

        path = Path(np.concatenate(vertices, axis=0), self._pathgen_codes(vertices))
        patch = PathPatch(path, facecolor=self.fillcolor, edgecolor=self.linecolor)
        ax.add_patch(patch)
        ax.update_datalim(path.vertices)

    def _pathgen_codes(self, vertices: List[Vertices]) -> List[int]:
        codes = []
        for verts in vertices:
            k = len(verts) - 1
            if k < 2:
                raise ValueError('Each segment needs at least 3 points.')
            codes.extend([Path.MOVETO, *((Path.LINETO,) * k)])
        return codes

    def _pathgen_downturn(
        self, x: float, y: float, dx: float, dy: float, last: bool=False
    ) -> Vertices:
        if last:
            xll, xlr = x - .5 * self.ribbon_width, x + .5 * self.ribbon_width
            xr = x + .5 * dx
            yl = y + dy
            return [
                [xlr, yl],
                [xll, yl],
                [xr, y],
                [xlr, yl],
            ]
        else:
            xll, xlr = x - .5 * self.ribbon_width, x + .5 * self.ribbon_width
            xrl, xrr = xll + dx, xlr + dx
            yl, yr = y + dy, y - dy
            return [
                [xlr, yl],
                [xll, yl],
                [xrl, yr],
                [xrr, yr],
                [xlr, yl],
            ]

    def _pathgen_upturn(self, left: Vertices, right: Vertices) -> Vertices:
        if len(left) == 1:
            lp = left[0].copy()
            rp0, rp1, rp2 = (right[i].copy() for i in range(3))
            rp0 = intersection(lp, rp0, rp1, rp2)
            verts = [lp, rp1, rp0, lp]
        elif len(right) == 1:
            lp2, lp3, lp4 = (left[i].copy() for i in range(2,5))
            rp = right[0].copy()
            lp2 = intersection(rp, lp2, lp3, lp4)
            verts = [rp, lp2, lp3, rp]
        else:
            lp2, lp3, lp4 = (left[i].copy() for i in range(2,5))
            rp0, rp1, rp2 = (right[i].copy() for i in range(3))
            lp2 = intersection(rp1, lp2, lp3, lp4)
            rp0 = intersection(lp3, rp0, rp1, rp2)
            verts = [lp3, lp2, rp1, rp0, lp3]
        return verts if self.fill_inner_ribbon else [*verts, *verts[-2::-1]]
        
    def get_legend_handle(self, drawstyle: DrawStyle) -> Rectangle:
        """Returns a handle for a legend, currently just a rectangle"""
        rec = Rectangle(
            (0.,0.), width=1., height=1.,
            linewidth = drawstyle.linewidth * self.linewidth_scalar,
            fill = (self.fillcolor is not None),
            edgecolor = self.linecolor, 
            facecolor = self.fillcolor,
        )
        return rec
    
    def to_dict(self) -> Dict[str, Any]:
        attrnames = ['fillcolor2', 'ribbon_period', 'fill_inner_ribbon']
        if self._ribbon_width is None:
            attrnames.append('ribbon_width')
        return super().to_dict(*attrnames)