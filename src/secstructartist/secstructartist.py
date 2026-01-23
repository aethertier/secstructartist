from __future__ import annotations
from pathlib import Path
from typing import Dict, Iterable, List, Literal, IO, Optional, Set, Tuple, Union, TYPE_CHECKING
from matplotlib.axes import Axes
from matplotlib.pyplot import subplots
from matplotlib.legend_handler import HandlerTuple
from .drawstyle import DrawStyle
from .utils import aggregate

if TYPE_CHECKING:
    from .elementartist import ElementArtist



class SecStructArtist():
    """
    Renderer for one-dimensional secondary structure schematics.

    This class provides a high-level interface for drawing secondary structure
    strings (e.g. ``"HHHHEEELL"``) into a Matplotlib Axes. Each secondary
    structure symbol is mapped to an :class:`ElementArtist` which controls
    how the corresponding element is rendered.
    """
    def __init__(
        self,
        elements: Optional[Dict[str,ElementArtist]] = None,
        **drawstyle_kwargs
    ):
        """
        Parameters
        ----------
        elements : dict of str to ElementArtist, optional
            Mapping from secondary structure symbols to element artists.

        **drawstyle_kwargs
            Keyword arguments forwarded to :class:`DrawStyle` to initialize
            the drawing style.
        """
        self._elements = dict(elements)
        self._drawstyle: DrawStyle = DrawStyle(**drawstyle_kwargs)
        self._drawn_elements: Set = set()
    
    @property
    def elements(self) -> Dict[str,ElementArtist]:
        """dict of str to ElementArtist"""
        return self._elements

    @property
    def drawstyle(self) -> DrawStyle:
        """DrawStyle: Current drawing style used for rendering."""
        return self._drawstyle
    
    def __getattr__(self, attrname):
        if not hasattr(self._drawstyle, attrname):
            raise AttributeError(f"{type(self).__name__!r} has no attribute {attrname!r}")
        return getattr(self._drawstyle, attrname)

    def __repr__(self) -> str:
        return f"SecStructArtist({list(self.elements.keys())})"
    
    def draw(
        self, 
        secstruct: Iterable[str] | str, 
        x: float = 1., y: float = 1., *, 
        ax: Optional[Axes] = None,
        **drawstyle_kwargs
    ):
        """
        Draw a secondary structure schematic.

        The secondary structure is rendered as a one-dimensional schematic in
        which consecutive residues with the same secondary-structure symbol
        are grouped and drawn as a single continuous element.

        Parameters
        ----------
        secstruct : str or iterable of str
            Residue-wise secondary structure symbols to be drawn. Each symbol
            must be present in ``self.elements``.

        x : float, default=1.0
            X-coordinate of the first residue.

        y : float, default=1.0
            Y-coordinate of the schematic baseline.

        ax : matplotlib.axes.Axes, optional
            Axes into which the schematic is drawn. If `None`, a new Axes is
            created.

        **drawstyle_kwargs
            Keyword arguments used to update the current :class:`DrawStyle`.

        Returns
        -------
        list
            List of Matplotlib artists created during drawing.
        """
        if drawstyle_kwargs:
            self.drawstyle = self.drawstyle.with_updates(**drawstyle_kwargs)
        if ax is None:
            fig, ax = subplots(figsize=(.1*len(secstruct),.5))
            ax.set_ylim([
                y - .7 * self.drawstyle.height, 
                y + .7 * self.drawstyle.height
            ])
            ax.set_xlim([
                x - .5 * self.drawstyle.step, 
                x + (len(secstruct) + .5) * self.drawstyle.step, 
            ])

        xpos = x
        drawn_elements = []
        for elem, elem_length in aggregate(secstruct):
            if elem not in self.elements:
                raise ValueError(f"Missing element artist for: '{elem}'")
            
            artist = self.elements[elem]
            drawn = artist.draw(xpos, y, length=elem_length, ax=ax, drawstyle=self.drawstyle)
            drawn_elements.extend(drawn)

            xpos += elem_length * self.drawstyle.step
            self._drawn_elements.add(elem)
        ax.autoscale_view()

        return drawn_elements
    
    def legend(self, *, ax: Axes, all_elements: bool=False, **legend_kwargs):
        """
        Add a legend for the rendered secondary structure elements.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Axes to which the legend is added.

        all_elements : bool, default=False
            If True, include all registered elements. If False, include only
            elements that have been drawn.

        **legend_kwargs
            Additional keyword arguments passed to ``Axes.legend``.

        Returns
        -------
        matplotlib.legend.Legend
            The created legend instance.
        """
        handles, labels = self.get_legend_handles_labels()
        print(handles, labels)
        legend = ax.legend(handles, labels, handler_map={tuple: HandlerTuple(ndivide=None)}, **legend_kwargs)
        legend.set_zorder(self.drawstyle.zorder + 1)
        return legend
    
    def get_legend_handles_labels(self, only_drawn_elements: bool=True) -> Tuple[List, List]:
        """
        Return legend handles and labels.

        Parameters
        ----------
        only_drawn_elements : bool, default=True
            If True, return handles only for elements that have been drawn.

        Returns
        -------
        handles : list
            List of legend handles.

        labels : list
            Corresponding legend labels.
        """
        handles, labels = [], []
        for elem, artist in self.elements.items():
            if only_drawn_elements and elem not in self._drawn_elements:
                continue
            hdl, lbl = artist.get_legend_handle_label(self.drawstyle)
            handles.append(hdl)
            labels.append(lbl)
        return handles, labels
    
    def reset_drawn_elements(self):
        """Reset the set of elements marked as drawn."""
        self._drawn_elements = set()

    def to_config(self, configfile: Optional[Union[Path, str]] = None):
        pass # TODO

    @classmethod
    def from_config(cls, configfile: Union[str, Path, IO[str]], format: Literal['json']) -> SecStructArtist:
        pass # TODO