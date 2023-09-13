from typing import Iterable
import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle
from .abc import ElementArtist
from ..utils.utils import DrawnSecStructElement


class LoopArtist(ElementArtist):
    """
    Class to draw loops

    Loops are represented by horizontal lines (if loop_height == 0), or
    rectangles (if loop_height > 0).

    Attributes:
    -----------
        height: float
            If set, loops are represented by rectangles of that height instead 
            of lines.
        linewidth: float   
            The boldness of the lines representing the loop. By default the 
            global linewisth is used.
        linecolor: color string or color tuple
            The color of the lines representing the loop. Any matplotlib-recognized 
            color option works, e.g., named colors, color tuples, hexstrings.
        fillcolor: color string or color tuple
            The color of the filling of the loop, if a rectangular loop is 
            drawn. Only used if `height` is set. (default: linecolor)

    Methods:
    --------
        draw(xpos, ypos, widths, ax)
            Draws a loop from `min(xpos)` to `max(xpos+widths)`.
    """
    
    ELEMENT = "Loop"

    def __init__(self, linecolor="k", fillcolor=None, height=None, 
                    linewidth=None, zorder=None, owner: "SecStructArtist" = None):
        super().__init__(height, linewidth, zorder, owner)
        self.linecolor = linecolor
        self.fillcolor = fillcolor or linecolor

    def draw(self, xpos: Iterable[float], ypos: float, widths, ax: Axes) -> DrawnSecStructElement:
        x0, x_ = np.min(xpos), np.max(xpos)
        if np.ndim(widths) > 0:
            assert len(widths) == len(xpos), "Widths and xpos must have the same number of elements."
            x1 = x_ + float(widths[len(xpos)-1])
        else:
            x1 = x_ + float(widths)

        if self._height is None:
            loop = self._draw_line(x0, x1, ypos, ax=ax)
            return DrawnSecStructElement(self.ELEMENT, x0, x_, lines=[loop])
        else:
            y0 = ypos-.5*self.height
            loop = self._draw_rectangle((x0,y0), x1-x0, self.height, ax=ax)
        return DrawnSecStructElement(self.ELEMENT, x0, x_, patches=[loop])

    def _draw_line(self, x0, x1, ypos, ax: Axes):
        """Draws a line from x0 to x1"""
        line = ax.plot([x0, x1], [ypos, ypos], color=self.linecolor, 
                       linewidth=self.linewidth, zorder=self.zorder-.1)
        return line

    def _draw_rectangle(self, xy, width, height, ax: Axes):
        """Draws a rectangle between (x0, y0) and (x1, y1)"""
        rect = Rectangle(xy, width, height, fill=True,
                        edgecolor=self.linecolor, linewidth=self.linewidth, 
                        facecolor=self.fillcolor, zorder=self.zorder-.1)
        ax.add_patch(rect)
        return rect