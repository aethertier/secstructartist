from __future__ import annotations
from typing import Any, Dict, Tuple, Union, TYPE_CHECKING
import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from .base import PrimitiveArtist

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from ..drawstyle import DrawStyle
    from ..typing_ import ColorType


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
        # self.fillcolor2 = fillcolor2
        self.ribbon_width = ribbon_width
        self.ribbon_period = ribbon_period
        self._vertices, self._codes = None, None

    @property
    def ribbon_width(self) -> float:
        if self._ribbon_width is None:
            return .4 * self.ribbon_period
        return self._ribbon_width
    
    @ribbon_width.setter
    def ribbon_width(self, value: float):
        self._ribbon_width = value

    def draw(self, x: float, y: float, length: int, ax: Axes, drawstyle: DrawStyle) -> Tuple[Polygon]:
        # Num of halfturns
        num_halfturns = int(max(1, round(2 * length / self.ribbon_period)))
        
        dx = drawstyle.step * length / num_halfturns 
        dy = drawstyle.height * self.height_scalar * .5
        
        self._path_init(x, y, dx=dx, dy=dy)
        x += .5 * dx
        i = 1
        for i in range(num_halfturns - 1):
            if i % 2:
                # self._path_add_upturn(x, y, dx, dy, upwards=bool(i%2))
                pass 
            else:
                self._path_add_downturn(x, y, dx, dy)





            # self._path_add_halfturn(x, y, dx, dy, upwards=bool(i%2))
            x += dx
        self._path_finalize(x, y, dx, dy, upwards=not bool(i%2))
        




        # self._init_path(x, y, dx=dx, dy=dy)
        # for _ in range(1, num_halfturns // 2):
        #     self._add_downturn_to_path(dx=dx, dy=dy)
        #     self._add_upturn_to_path(dx=dx, dy=dy)
        #     x += 2 * dx
        # self._add_downturn_to_path(dx=dx, dy=dy)
        # if num_halfturns % 2 == 1:
        #     self._add_upturn_to_path(dx=dx, dy=dy)
        #     self._finalize_path(dx=dx, dy=dy, upturn=False)
        # else:
        #     self._finalize_path(dx=dx, dy=dy, upturn=True)
        # # self._add_upturns_to_path(x, y, n_turns=int(num_halfturns // 2), dx=width, dy=height)
        # # self._add_downturns_to_path(x, y, n_turns=int(num_halfturns // 2), dx=width, dy=height)
        # # xpos = x
        # # for i in range(int(num_halfturns // 2)):
        # #     self._add_ribbon1(xpos, y, halfturn, height)
        # #     xpos += 2 * halfturn
        
        print(np.concatenate(self._vertices, axis=0).shape)
        print(np.concatenate(self._codes, axis=0).shape)
        path = Path(np.concatenate(self._vertices, axis=0), np.concatenate(self._codes, axis=0))
        patch = PathPatch(path, facecolor=self.fillcolor, edgecolor=self.linecolor)
        ax.add_patch(patch)
        ax.update_datalim(path.vertices)

    def _path_init(self, x: float, y: float, dx:float, dy: float):
        x1 = x + .5 * (dx +  self.ribbon_width)
        x2 = (dx**2 + self.ribbon_width * dx) / (4 * dx + 2 * self.ribbon_width)
        y1 = y + dy
        y2 = y1 - 2 * dy * 
            
        ]
        p3 = [x + .5 * (dx + self.ribbon_width), y + dy]
        self._vertices = [p1, p2, p3, p1]
        self._codes = [
            [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
        ]

    def _path_add_downturn(self, x: float, y: float, dx:float, dy: float):


        xr0, xr1 = x + .5 * (dx - self.ribbon_width), x + .5 * (dx + self.ribbon_width)
        yr = y + dy
        self._vertices = [
            [[x, y], [xr0, yr], [xr1, yr], [x, y]]
        ]
        self._codes = [
            [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
        ]

    def _path_add_downturn(self, x: float, y: float, dx:float, dy: float):
        xl0, xl1 = x - .5 * self.ribbon_width, x + .5 * self.ribbon_width
        xr0, xr1 = xl0 + dx, xl1 + dx
        yl, yr = y + dy, y - dy
        self._vertices.append([
            [xl0, yl],
            [xr0, yr],
            [xr1, yr],
            [xl1, yl],
            [xl0, yl]
        ])
        self._codes.append([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
        ])

    def _path_finalize(self, x: float, y: float, dx:float, dy: float, upwards: bool):
        xl0, xl1 = x - .5 * self.ribbon_width, x + .5 * self.ribbon_width
        xr = x + .5 * dx
        yl = y - dy if upwards else y + dy
        self._vertices.append([
            [xr, y],
            [xl1, yl],
            [xl0, yl],
            [xr, y]
        ])
        self._codes.append([
            Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY
        ])


    def get_legend_handle(self, drawstyle: DrawStyle) -> Polygon:
        # Define a small, normalized arrow in legend coordinates
        # Legend handles typically live in a ~1x1 box
        # xypath = [
        #     (0.0, 0.3),
        #     (0.6, 0.3),
        #     (0.6, 0.1),
        #     (1.0, 0.5),
        #     (0.6, 0.9),
        #     (0.6, 0.7),
        #     (0.0, 0.7),
        # ]
        # sheet = Polygon(xypath, closed=True, 
        #     linewidth = drawstyle.linewidth * self.linewidth_scalar,
        #     fill = (self.fillcolor is not None),
        #     edgecolor = self.linecolor, 
        #     facecolor = self.fillcolor,
        # )
        # return sheet
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        attrnames = ['fillcolor2', 'ribbon_period']
        if self._ribbon_width is None:
            attrnames.append('ribbon_width')
        return super().to_dict(*attrnames)