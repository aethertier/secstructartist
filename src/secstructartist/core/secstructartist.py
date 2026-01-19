from pathlib import Path
from typing import Dict, Set, Iterable, Optional, Union
from matplotlib.axes import Axes
from matplotlib.pyplot import subplots

from .drawstyle import DrawStyle
from .elementartist import ElementArtist
from .utils import aggregate


class SecStructArtist():
    """Class to draw secondary structure representations

    All secondary structure representations are typically drawn in an existing
    maplotlib axis.
    """
    def __init__(
        self,
        artists: Optional[Dict[str,ElementArtist]] = None,
        **drawstyle_kwargs
    ):
        self._artists = dict(artists)
        self._drawstyle: DrawStyle = DrawStyle(**drawstyle_kwargs)
        self._drawn_elements: Set = set()
    
    @property
    def artists(self) -> Dict[str,ElementArtist]:
        return self._artists

    @property
    def drawstyle(self) -> DrawStyle:
        return self._drawstyle
    
    def __getattr__(self, attrname):
        if not hasattr(self._drawstyle, attrname):
            raise AttributeError(f"{type(self).__name__!r} has no attribute {attrname!r}")
        return getattr(self._drawstyle, attrname)

    def __repr__(self) -> str:
        return f"SecStructArtist({list(self.artists.keys())})"
    
    def draw(
        self, 
        secstruct: Iterable[str] | str, 
        x: float = 1., y: float = 1., *, 
        ax: Optional[Axes] = None,
        **drawstyle_kwargs
    ): 
        """
        Draws the secondary structure schema into the axis.

        The secondary structure is rendered as a one-dimensional schematic,
        where each residue is represented by a graphical element defined by
        the selected :class:`SecStructArtist`. Consecutive residues with the
        same secondary-structure label are grouped and drawn as a single
        continuous element

        Parameters
        ----------
        secstruct : str or Iterable[str]
            Residue-wise secondary structure lables to be drawn. Every label
            should be present in the self.artists dictionary.

        x : float
            The position of the first residue in the x-axis. (default: 1.)

        y : float
            The position of the first residue in the y-axis. (default: 1.)
        
        ax : Axes
            Matplotlib Axes the scheme will be drawn to. If `None` a new Axes
            object will be created.

        **drawstyle_kwargs
            DrawStyle keywords like `linewidth`, `height`, `step`, or `zorder`.
            The scheme will be draw with the modified drawstyle, without altering
            the attribute in SecStructAritst.
        """
        # Create local drawstyle
        drawstyle = self.drawstyle.with_updates(**drawstyle_kwargs)
        if ax is None:
            fig, ax = subplots(figsize=(.1*len(secstruct),.5))
            ax.set_ylim([y - .7 * drawstyle.height, y + .7 * drawstyle.height])

        xpos = x
        drawn_elements = []
        for elem, elem_length in aggregate(secstruct):
            if elem not in self.artists:
                raise ValueError(f"Missing element artist for: '{elem}'")
            
            artist = self.artists[elem]
            drawn = artist.draw(xpos, y, length=elem_length, ax=ax, drawstyle=drawstyle)
            drawn_elements.append(drawn)

            xpos += elem_length * drawstyle.step
            self._drawn_elements.add(elem)

        return drawn_elements

    def reset_drawn_elements(self):
        self._drawn_elements = set()

    def to_config(self, configfile: Optional[Union[Path, str]] = None):
        pass # TODO

    @classmethod
    def from_config(cls, configfile: Path | str):
        # configpath = Path(configfile)
        # if not configpath.exists():
        #     raise FileNotFoundError(f"Cannot find configuration file: '{configpath}'")
        pass # TODO