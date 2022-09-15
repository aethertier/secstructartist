"""
secstructartist

Author: David Bickel (david.bickel@vub.be)
Date:   29/08/2022

The module to plot secondary structure representations in normal matplotlib 
plots. The secondary structure is given as a string with one character per 
residue:
    H ... helix
    S ... sheet/extended
    L ... loop
    
These strings can be generated, e.g., in PyMOL by the one-liner:
    >> iterate n. CA, print(ss, end="")

Usage:

    import matplotlib.pyplot as plt
    from secstructartist import SecStructArtist


    # Initialize figure with axis
    fig, ax = plt.subplots()
    
    # Plot secondary structure at point (x=18, y=0.75)
    SSA = SecStructArtist()
    SSA.set(
        height=.5, 
    )
    SSA.draw(18, .75, "LLSSSSSLLLHHHHLL", ax)
"""

from abc import ABCMeta, abstractmethod
import itertools as it

from matplotlib.axes import Axes


class SecStructArtist:
    """
    Class to draw secondary structure representations

    All secondary structure representations are typically drawn in an existing
    maplotlib axis.

    Attributes:
    -----------

        LoopArtist: object  
                            An ElementArtist object that realizes the drawing 
                            of loops. Its attributes are typically prefixed 
                            "loop_" and can be set through the set() method.

        HelixArtist : object
                            An ElementArtist object that realizes the drawing 
                            of helices. Its attributes are typically prefixed 
                            "helix_" and can be set through the set() method.

        SheetArtist: object
                            An ElementArtist object that realizes the drawing 
                            of sheets. Its attributes are typically prefixed 
                            "sheet_" and can be set through the set() method.


        height: float       The overall height of secondary structure elements
                            to be drawn. Can be overwritten within the 
                            ElementArtists, to customize the height of 
                            secondary structure elements individually.

        fancy_helices: boolean
                            Whether to draw helices "fancy" or not.

    Methods:
    --------

        set(): attribute_name = value or **kwargs
                            Sets the attributes controlling the way, plots are 
                            drawn. All attributs of the ElementArtists can be
                            set as well.

        get(): attribute_name or None
                            Gets the current value of the given attribute.
                            If no attribute_name is given, a dict with the
                            current values for all attributes is returned.

        draw(self, x, y, secstruct_str: str, axis):
                            Draws secondary structure elements, as indicated by
                            secstruct_str. Horizontally, the scheme is drawn 
                            from (x) till (x + len(secstruct_str) - 1).
                            Vertically, the scheme is draw from 
                            (y - .5 * height) to (y + .5 * height).
    """

    def __init__(self, **kwargs):

        self.LoopArtist = SecStructLoopArtist(self)
        self.HelixArtist = SecStructHelixArtist(self)
        self.SheetArtist = SecStructSheetArtist(self)
        self.height = 1.
        self.linewidth = 1.
        self.fancy_helices = True
        self.zorder = 5
        self.set(**kwargs)

    def get(self, attr_name: str = None):
        """ Returns the current values of attributes """

        if attr_name is None:
            outdict = {}
            for attrname, attrvalue in self.__dict__.items():
                if attrname.endswith("Artist"):
                    outdict.update( getattr(self, attrname).get() )
                elif attrname.startswith("_"):
                    pass
                else:
                    outdict[attrname] = attrvalue
            return outdict

        else:
            if attr_name.startswith("loop_"):
                return getattr(self.LoopArtist, attr_name)
            elif attr_name.startswith("sheet_"):
                return getattr(self.SheetArtist, attr_name)
            elif attr_name.startswith("helix_"):
                return getattr(self.HelixArtist, attr_name)
            else:
                return getattr(self, attr_name)

    def set(self, **kwargs):
        """ Sets one or more attributes """

        for attr_name, attr_value in kwargs.items():
            if attr_name.startswith("loop_"):
                self.LoopArtist.set(**{attr_name: attr_value})
            elif attr_name.startswith("sheet_"):
                self.SheetArtist.set(**{attr_name: attr_value})
            elif attr_name.startswith("helix_"):
                self.HelixArtist.set(**{attr_name: attr_value})
            else:
                setattr(self, attr_name, attr_value)

    def draw(self, x, y, secstruct_str, axis: Axes):
        """ DOC STRING """

        ssgenerator = ((k, len(list(g))) for k,g in it.groupby(secstruct_str))
        sselements  = []

        for sstype, sslength in ssgenerator:
            if sstype == 'L':
                sselements.append(
                    self.LoopArtist.draw(x, y, sslength, axis))
            elif sstype == 'S':
                sselements.append(
                    self.SheetArtist.draw(x, y, sslength, axis))
            elif sstype == 'H':
                sselements.append(
                    self.HelixArtist.draw(x, y, sslength, axis))
            x += sslength

        return sselements



class SecStructElementArtist(metaclass=ABCMeta):
    """ Abstract class for drawing secondary structure elements """

    def __init__(self, parentObj: SecStructArtist, **kwargs):
        self._parent = parentObj

    @property
    @abstractmethod
    def height(self):
        pass

    @property
    @abstractmethod
    def linewidth(self):
        pass
    
    @property
    def zorder(self):
        return self._parent.zorder

    def get(self, attr_name = None):
        """ Returns the current values of attributes """
        if attr_name is None:
            return {n:v for n,v in self.__dict__.items() if not n.startswith("_")}
        else:
            return getattr(self, attr_name)

    def set(self, **kwargs):
        """ Sets an attribute to a value """
        for attr_name, attr_value in kwargs.items():
            if hasattr(self, attr_name):
                setattr(self, attr_name, attr_value)
            else:
                raise AttributeError(f"Unable to set attribute: {self.__class__.__name__} has not attribute '{attr_name}'.")

    @abstractmethod
    def draw(self, x: float, y: float, length: float, ax: Axes) -> tuple:
        pass
    
    @staticmethod
    def collect_drawn_elements(draw_function) -> dict:

        def wrapper(self, x: float, y: float, length: float, ax: Axes):
            outdict = dict(
                type = self.__class__.typestr,
                resid_start = x,
                resid_end = x + length - 1,
                lines = None,
                collections = None)
            l_drawn, c_drawn = draw_function(self, x, y, length, ax)
            outdict["lines"] = l_drawn
            outdict["collections"] = c_drawn
            return outdict
        
        return wrapper
        

class SecStructLoopArtist(SecStructElementArtist):
    """
    Class to draw loops

    Loops are represented by horizontal lines (if loop_height == 0), or
    rectangles (if loop_height > 0).

    Attributes:
    -----------

        loop_height: float      If set, loops are represented by rectangles of 
                                that height instead of lines.
                                
        loop_linewidth: float   The boldness of the lines representing the 
                                loop. By default the global linewisth is used.

        loop_linecolor: color string or color tuple
                                The color of the lines representing the loop.
                                Any matplotlib-recognized color option works,
                                e.g. named colors, color tuples, hexstrings.

        loop_fillcolor: color string or color tuple
                                The color of the filling of the loop, if a
                                rectangular loop is drawn. Only used if 
                                loop_height is set.


    Methods:
    --------

        draw(x, y, length, ax)  Draws a loop from (x-.5) to (x+length-.5) in 
                                axis ax. The y refers to the vertical center
                                of the loop.    
    """
    
    typestr = "loop"

    def __init__(self, parentObj: SecStructArtist):
        super().__init__(parentObj)
        self.loop_height = None
        self.loop_linewidth = None
        self.loop_linecolor = 'k'
        self.loop_fillcolor = "k"

    @property
    def height(self):
        if self.loop_height is not None:
            return self.loop_height
        return self._parent.height

    @property
    def linewidth(self):
        if self.loop_linewidth is not None:
            return self.loop_linewidth
        return self._parent.linewidth
        

    @SecStructElementArtist.collect_drawn_elements
    def draw(self, x: float, y: float, length: float, ax: Axes) -> dict:

        lines_drawn = []
        collections_drawn = []

        x0, x1 = x-.5, x+length-.5

        if self.loop_height is None:
            lines_drawn += ax.plot([x0, x1], [y, y],
                color=self.loop_linecolor, linewidth=self.linewidth, zorder=self.zorder - 2)                
        else:
            y0, y1 = y - .5*self.height, y + .5*self.height
            lines_drawn += ax.plot(
                [x0, x1, x1, x0, x0], [y1, y1, y0, y0, y1],
                color=self.loop_linecolor, linewidth=self.linewidth, zorder=self.zorder - 2)
            collections_drawn.append(
                ax.fill_between(
                    [x0, x1], [y0, y0], [y1, y1],
                    color=self.loop_fillcolor, zorder=self.zorder - 3))
        
        return lines_drawn, collections_drawn


class SecStructSheetArtist(SecStructElementArtist):
    """
    Class to draw sheets 
    
    Sheets are represented by a rectangular body ending in an arrow pointing 
    towards the C-terminus. 

    Attributes:
    -----------

        sheet_height: float     If set, sheets use that value instead of the 
                                global height.

        sheet_hratio: float     The relative height of the rectangular body 
                                with respect to the arrow part. [default: 0.7]
                                If set to 1.0, body and arrow part will have 
                                the same height.

        sheet_arrowlength: float
                                The length of the arrow part of the sheet on the
                                x-axis. If a sheet segment is shorter than this, 
                                no rectangular body is drawn (default: 5).

        sheet_linewidth: float  The width of the edges in the representation. 
                                By default the global linewidth is used.

        sheet_linecolor: color string or color tuple  
                                The color of the edges of the sheet 
                                representation (default = 'k').

        sheet_fillcolor: color string or color tuple 
                                The color of the filling of the sheet
                                representation.

    Methods:
    --------

        draw(x, y, length, ax)  Draws a sheet from (x-.5) to (x+length-.5) in 
                                axis ax. The y refers to the vertical center
                                of the sheet.    
    """

    typestr = "sheet"

    def __init__(self, parentObj):
        super().__init__(parentObj)
        self.sheet_height = None
        self.sheet_linewidth = None
        self.sheet_hratio    =  .7
        self.sheet_arrowlength = 5
        self.sheet_linecolor = 'k'
        self.sheet_fillcolor = "0.97"

    @property
    def height(self):
        if self.sheet_height is None:
            return self._parent.height
        return self.sheet_height

    @property
    def linewidth(self):
        if self.sheet_linewidth is not None:
            return self.sheet_linewidth
        return self._parent.linewidth

    @SecStructElementArtist.collect_drawn_elements
    def draw(self, x: float, y: float, length: float, ax: Axes) -> dict:

        lines_drawn = []
        collections_drawn = []

        x0, x1, x2 = (\
            x - .5,
            x + length - self.sheet_arrowlength - .5, 
            x + length - .5 )
        y0, y1, y2, y3, y4 = (\
            y - .5 * self.height,
            y - .5 * self.sheet_hratio * self.height,
            y,
            y + .5 * self.sheet_hratio * self.height,
            y + .5 * self.height)

        if x1 <= x0:
            lines_drawn += ax.plot(
                [x0,x2,x0,x0], [y4,y2,y0,y4],
                linewidth=self.linewidth, color=self.sheet_linecolor, zorder=self.zorder)
            collections_drawn.append(
                ax.fill_between(
                    [x0, x2], [y0, y2], [y4, y2],
                    color=self.sheet_fillcolor, zorder=self.zorder-1))
        else:
            lines_drawn += ax.plot(
                [x0, x0, x1, x1, x2, x1, x1, x0],
                [y1, y3, y3, y4, y2, y0, y1, y1],
                linewidth=self.linewidth, color=self.sheet_linecolor, zorder=self.zorder)
            collections_drawn.append( 
                ax.fill_between(
                    [x0, x1, x1, x2], [y1, y1, y0, y2], [y3, y3, y4, y2],
                    color=self.sheet_fillcolor, zorder=self.zorder-1))
        
        return lines_drawn, collections_drawn


class SecStructHelixArtist(SecStructElementArtist):
    """
    Class to draw helices 
    
    Helices are represented, either by a single rectangle (fancy_helices == False) 
    or sets of small rectangles mimicking a helix. 

    Attributes:
    -----------

        helix_height: float     If set, helices use that value instead of the 
                                global height.

        helix_turnlength: float
                                The x intervall over which the drawn helix 
                                should represent one turn. This is adapted
                                dynamically to always end in vertical bars.

        helix_linewidth: float  The width of the edges in the representation. 
                                By default the global linewidth is used.

        helix_linecolor: color string or color tuple  
                                The color of the edges of the helix 
                                representation (default = 'k').

        helix_fillcolor: color string or color tuple 
                                The color of the filling of the helix
                                representation.

        helix_fillcolor2: color string or color tuple 
                                The color of the filling of the diagonal bars
                                in the helix representation (fancy helices only).

    Methods:
    --------

        draw(x, y, length, ax)  Draws a sheet from (x-.5) to (x+length-.5) in 
                                axis ax. The y refers to the vertical center
                                of the sheet.    
    """

    typestr = "helix"

    def __init__(self, parentObj):
        super().__init__(parentObj)
        self.helix_cartoonwidthfraction = .38
        self.helix_height     = None
        self.helix_linewidth  = None
        self.helix_turnlength = 3.6
        self.helix_linecolor  = 'k'
        self.helix_fillcolor  = "0.97"
        self.helix_fillcolor2 = "0.8"

    @property
    def height(self):
        if self.helix_height == None:
            return self._parent.height
        return self.helix_height

    @property
    def linewidth(self):
        if self.helix_linewidth is not None:
            return self.helix_linewidth
        return self._parent.linewidth

    @SecStructElementArtist.collect_drawn_elements
    def draw(self, x: float, y: float, length: float, ax: Axes) -> dict:
        if self._parent.fancy_helices:
            return self._draw_fancy(x, y, length, ax)
        else:
            return self._draw_simple(x, y, length, ax)

    def _draw_simple(self, x: float, y: float, length: float, ax: Axes):

        lines_drawn = []
        collections_drawn = []

        x0, x1 = x - .5, x -.5 + length
        y0, y1 = y - .5 * self.height, y + .5 * self.height

        lines_drawn += ax.plot(
            [x0, x0, x1, x1, x0], [y0, y1, y1, y0, y0],
            color=self.helix_linecolor, linewidth=self.linewidth, 
            zorder=self.zorder - 1)
        collections_drawn.append(
            ax.fill_between(
                [x0, x1], [y0, y0], [y1, y1],
                color=self.helix_fillcolor, zorder=self.zorder-1))
        
        return lines_drawn, collections_drawn

    def _draw_fancy(self, x: float, y: float, length: float, ax: Axes):

        lines_drawn = []
        collections_drawn = []

        width = self.helix_cartoonwidthfraction * self.helix_turnlength
        repeats    = max(1, round(length / self.helix_turnlength))
        xintervall =  (length - width) / repeats
        y0, y1, y2, y3 = (\
            y - .5 * self.height,
            y + self.height * (.5 - (xintervall - width) / xintervall),
            y - self.height * (.5 - (xintervall - width) / xintervall),
            y + .5 * self.height)
        x0 = x - .5

        for i in range(repeats):
            x1, x2 = x0 + width, x0 + xintervall
            lines_drawn += ax.plot([x1, x0, x0, x1, x1],
                                   [y3, y3, y0, y0, y3],
                                   color=self.helix_linecolor, 
                                   linewidth=self.linewidth,
                                   zorder=self.zorder)
            collections_drawn.append(
                ax.fill_between([x0, x1], [y0, y0], [y3, y3],
                                color=self.helix_fillcolor,
                                zorder=self.zorder-1)
            )
            lines_drawn += ax.plot([x1, x2, x2, x1],
                                   [y3, y1, y0, y2],
                                   color=self.helix_linecolor, 
                                   linewidth=self.linewidth,
                                   zorder=self.zorder-2)
            collections_drawn.append(
                ax.fill_between([x1, x2], [y2, y0], [y3, y1],
                                color=self.helix_fillcolor2,
                                zorder=self.zorder-3))
            x0 = x2
        else:
            x1 = x0 + width
            lines_drawn += ax.plot([x1, x0, x0, x1, x1],
                                   [y3, y3, y0, y0, y3],
                                   color=self.helix_linecolor, 
                                   linewidth=self.linewidth,
                                   zorder=self.zorder)
            collections_drawn.append(
                ax.fill_between([x0, x1], [y0, y0], [y3, y3],
                                color=self.helix_fillcolor,
                                zorder=self.zorder-1))
        
        return lines_drawn, collections_drawn
        