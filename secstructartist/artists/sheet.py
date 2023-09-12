from typing import Iterable
import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Polygon
from .abc import ElementArtist
from ..utils.utils import DrawnSecStructElement


class SheetArtist(ElementArtist):
    """
    Class to draw sheets 
    
    Sheets are represented by a rectangular body ending in an arrow pointing 
    towards the C-terminus. 

    Attributes:
    -----------
        height: float 
            If set, sheets use that value instead of the global height.
        linewidth: float
            The width of the edges in the representation. By default the global 
            linewidth is used.
        arrow_length: float
            The length of the arrow part of the sheet in terms of residues. If a
            sheet segment is shorter than this, no rectangular body is drawn 
            (default: 5).
        arrow_ratio: float
            The relative height of the rectangular body with respect to the 
            arrow part. [default: 0.7] If set to 1.0, body and arrow part will 
            have the same height.
        linecolor: color string or color tuple  
            The color of the edges of the sheet representation (default = 'k').
        fillcolor: color string or color tuple 
            The color of the filling of the sheet representation.

    Methods:
    --------
        draw(xpos, ypos, widths, ax) -> DrawnSecStructElement:
            Draws a sheet from `min(xpos[0])` to `max(xpos+widths)`.
    """

    ELEMENT = "Sheet"

    def __init__(self, arrow_length: int = 5,
                 arrow_ratio: float = .7, linecolor="k", fillcolor="0.97", 
                 height=None, linewidth=None, zorder=None, owner: "SecStructArtist" = None):
        super().__init__(height, linewidth, zorder, owner)
        self.arrow_length = arrow_length
        self.arrow_ratio = arrow_ratio
        self.linecolor = linecolor
        self.fillcolor = fillcolor

    def draw(self, xpos: Iterable[float], ypos: float, widths: 1, ax: Axes) -> DrawnSecStructElement:
        
        x0, x_ = np.min(xpos), np.max(xpos)
        if np.ndim(widths) > 0:
            assert len(widths) == len(xpos), "Widths and xpos must have the same number of elements."
            x2 = x_ + float(widths[len(xpos)-1])
        else:
            x2 = x_ + float(widths)
        
        y0, y1, y2, y3, y4 = (
            ypos - .5 * self.height, 
            ypos - .5 * self.arrow_ratio * self.height, 
            ypos,
            ypos + .5 * self.arrow_ratio * self.height, 
            ypos + .5 * self.height
        )  

        # Path for only the arrow head
        if self.arrow_length >= len(xpos):
            xpth, ypth = [x0, x2, x0], [y4, y2, y0]
            
        # Path for arrow with shaft
        else:
            i = int(np.ceil(self.arrow_length))
            x1 = xpos[-i]
            x1 += (i - self.arrow_length) * (x2 - x1) # in case arrow_length is a fraction
            xpth, ypth = [x0, x1, x1, x2, x1, x1, x0], [y1, y1, y0, y2, y4, y3, y3]

        sheet = Polygon(np.stack([xpth, ypth], axis=1), closed=True, fill=True,
                        edgecolor=self.linecolor, linewidth=self.linewidth, 
                        facecolor=self.fillcolor, zorder=self.zorder)
        ax.add_patch(sheet)
        return DrawnSecStructElement(self.ELEMENT, x0, x_, patches=[sheet])