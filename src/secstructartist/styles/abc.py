import abc
from typing import Iterable
from matplotlib.axes import Axes
from ..utils.utils import DrawnSecStructElement


class ElementArtist(metaclass=abc.ABCMeta):
    """ Abstract class for artists that draw individual secondary structure elements """

    ELEMENT = ""

    def __init__(self, height=None, linewidth=None, zorder=None, owner: "SecStructArtist" = None):
        self.owner = owner
        self.height = height
        self.linewidth = linewidth
        self.zorder = zorder

    @property
    def height(self):
        return self._height or self.owner.height
    
    @height.setter
    def height(self, height):
        self._height = height

    @property
    def linewidth(self):
        return self._linewidth or self.owner.linewidth
    
    @linewidth.setter
    def linewidth(self, linewidth):
        self._linewidth = linewidth

    @property
    def zorder(self):
        return self._zorder or self.owner.zorder
    
    @zorder.setter
    def zorder(self, zorder):
        self._zorder = zorder

    @abc.abstractmethod
    def draw(self, xpos: Iterable[float], ypos: float, widths, ax: Axes) -> DrawnSecStructElement:
        pass


class BlankArtist(ElementArtist):
    """Secondary structure artist invoked for unknown secondary structure codes.
    This artist does not draw anything, leaving a blank space in the plot"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BlankArtist, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, height=42, linewidth=42, zorder=42, owner: "SecStructArtist" = None):
        super().__init__(height, linewidth, zorder, owner)
    
    def draw(self, xpos: Iterable[float], ypos: float, widths, ax: Axes) -> DrawnSecStructElement:
        return DrawnSecStructElement("N/A")
