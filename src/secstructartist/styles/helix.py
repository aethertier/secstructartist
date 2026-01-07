from itertools import cycle
from typing import Iterable
import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Polygon
from .abc import ElementArtist
from ..utils.utils import DrawnSecStructElement


class HelixArtist(ElementArtist):
    """
    Class to draw helices 
    
    Helices are represented, either by a single rectangle

    Attributes:
    -----------
        height: float
            If set, helices use that value instead of the global height.
        linewidth: float
            The width of the edges in the representation. By default the global 
            linewidth is used.
        linecolor: color string or color tuple  
            The color of the edges of the helix representation (default: 'k').
        fillcolor: color string or color tuple 
            The color of _outward_ loops in the helix representation. (default: '0.97')
        shadecolor: color string or color tuple
            The color of _inward_ loops in the helix representation. (default: '0.80')
    
    Methods:
    --------
        draw(xpos, ypos, widths, ax)
            Draws a loop from `min(xpos)` to `max(xpos+widths)`.
    """

    ELEMENT = "Helix"

    def __init__(self, linecolor="k", fillcolor="0.97", shadecolor = "0.8", 
                    ribbon_width = None, ribbon_period = 3.6, height=None, 
                    linewidth=None, zorder=None, owner: "SecStructArtist" = None):
        super().__init__(height, linewidth, zorder, owner)
        self.linecolor = linecolor
        self.fillcolor = fillcolor
        self.shadecolor = shadecolor
        self.ribbon_width = ribbon_width or .3 * ribbon_period
        self.ribbon_period = ribbon_period
        

    def draw(self, xpos: Iterable[float], ypos: float, widths, ax: Axes) -> DrawnSecStructElement:
        
        # Get x limits of the turns
        x0, x_ = np.min(xpos), np.max(xpos)
        if np.ndim(widths) > 0:
            assert len(widths) == len(xpos), "Widths and xpos must have the same number of elements."
            x1 = x_ + float(widths[len(xpos)-1])
        else:
            x1 = x_ + float(widths)

        # Number of turns to draw, rounded to half-turns
        n_halfturns = round(2 * len(xpos) / self.ribbon_period)
        xvals = np.linspace(x0, x1, n_halfturns * 7 + 1)

        # Draw helix ribon element by element
        i, j = 0, 3
        patches = [self._init_ribbon(xvals[i], xvals[j], ypos)]
        for (updwn, width) in cycle([("downward", 8), ("upward", 6)]):
            i, j = j, j + width
            if j < xvals.size:
                patches.append(
                    getattr(self, f"_{updwn}_ribbon")(xvals[i], xvals[j], ypos))
            else:
                patches.append(
                    getattr(self, f"_{updwn}_ribbon_end")(xvals[i], xvals[-1], ypos))
                break
        # Add polygons to axis
        for poly in patches: ax.add_patch(poly)
        return DrawnSecStructElement(self.ELEMENT, x0, x_, patches=patches)

    def _init_ribbon(self, x0, x1, ypos):
        wdt, hgt = .5 * self.ribbon_width, .5 * self.height
        crds = [[x0, ypos],
                [x1 + wdt, ypos + hgt],
                [x1 - wdt, ypos + hgt]]
        poly = Polygon(crds, closed=True, fill=True,
                        edgecolor=self.linecolor, linewidth=self.linewidth, 
                        facecolor=self.shadecolor, zorder=self.zorder-.1)
        return poly
    
    def _upward_ribbon(self, x0, x1, ypos):
        """Draws ribbon for 6/14 of the full leng"""
        wdt, hgt = .5 * self.ribbon_width, .5 * self.height
        crds = [[x0 - wdt, ypos - hgt],
                [x0 + wdt, ypos - hgt],
                [x1 + wdt, ypos + hgt],
                [x1 - wdt, ypos + hgt]]
        poly = Polygon(crds, closed=True, fill=True,
                        edgecolor=self.linecolor, linewidth=self.linewidth, 
                        facecolor=self.shadecolor, zorder=self.zorder-.1)
        return poly

    def _upward_ribbon_end(self, x0, x1, ypos):
        """Draws ribbon for 3/14 of the full turn width"""
        wdt, hgt = .5 * self.ribbon_width, .5 * self.height
        crds = [[x0 - wdt, ypos - hgt],
                [x0 + wdt, ypos - hgt],
                [x1, ypos]]                
        poly = Polygon(crds, closed=True, fill=True,
                        edgecolor=self.linecolor, linewidth=self.linewidth, 
                        facecolor=self.shadecolor, zorder=self.zorder-.1)
        return poly
    
    def _downward_ribbon(self, x0, x1, ypos):
        """Draws ribbon for 8/14 of the full length"""
        wdt, hgt = .5 * self.ribbon_width, .5 * self.height
        crds = [[x0 - wdt, ypos + hgt],
                [x0 + wdt, ypos + hgt],
                [x1 + wdt, ypos - hgt],
                [x1 - wdt, ypos - hgt]]
        poly = Polygon(crds, closed=True, fill=True,
                        edgecolor=self.linecolor, linewidth=self.linewidth, 
                        facecolor=self.fillcolor, zorder=self.zorder)
        return poly

    def _downward_ribbon_end(self, x0, x1, ypos):
        """Draws ribbon for 4/14 of the full leng"""
        wdt, hgt = .5 * self.ribbon_width, .5 * self.height
        crds = [[x0 - wdt, ypos + hgt],
                [x0 + wdt, ypos + hgt],
                [x1, ypos],]
        poly = Polygon(crds, closed=True, fill=True,
                        edgecolor=self.linecolor, linewidth=self.linewidth, 
                        facecolor=self.fillcolor, zorder=self.zorder)
        return poly
