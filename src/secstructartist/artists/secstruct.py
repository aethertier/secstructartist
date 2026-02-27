from __future__ import annotations
from typing import (
    Dict, Generator, Iterable, List, Literal, Optional, Set, Tuple, Union, TYPE_CHECKING
)
from matplotlib.legend_handler import HandlerTuple
from .drawstyle import DrawStyle

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from .element import ElementArtist
    from ..typing_ import ArtistKW, PathOrFile, FileFormat, DrawnArtist, LegendHandlesLabels

def _aggregate(x: Iterable[str], /) -> Generator[Tuple[str, int], None, None]:
    """Aggregate consecutive identical elements and count their occurrences."""
    xiter = iter(x)
    try:
        xval, xcnt = next(xiter), 1
    except StopIteration:
        return
    for xi in xiter:
        if xi == xval:
            xcnt += 1
        else:
            yield xval, xcnt
            xval, xcnt = xi, 1
    yield xval, xcnt


class SecStructArtist():
    """
    Renderer for one-dimensional secondary structure schematics.

    This class provides a high-level interface for drawing secondary structure
    strings (e.g. ``"LLHHHHHLLEEE"``) into a Matplotlib Axes. Each secondary
    structure symbol is mapped to an :class:`ElementArtist` which controls
    how the corresponding element is rendered.
    """
    def __init__(
        self,
        elements: Optional[Dict[str, ElementArtist]] = None,
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
    def elements(self) -> Dict[str, ElementArtist]:
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
        secstruct: Iterable[str], 
        x: float = 1., 
        y: float = 1., 
        ax: Axes = None,
        **drawstyle_kwargs
    ) -> List[DrawnArtist]:
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

        ax : matplotlib.axes.Axes
            Axes into which the schematic is drawn. Mandatory when calling 
            ``draw`` directly.

        **drawstyle_kwargs
            Keyword arguments that update current :class:`DrawStyle`.

        Returns
        -------
        list
            List of Matplotlib artists created during drawing.
        """
        if drawstyle_kwargs:
            self.update_drawstyle(**drawstyle_kwargs)
        if ax is None: 
            raise ValueError(
                'draw() requires a matplotlib.axes.Axes. Use draw_secondary_structure() '
                'convenience function to create one automatically.'
            )

        xpos = x
        drawn_elements = []
        for elem, elem_length in _aggregate(secstruct):
            if elem not in self.elements:
                raise ValueError(f"Missing element artist for: '{elem}'")
            
            artist = self.elements[elem]
            drawn = artist.draw(xpos, y, length=elem_length, ax=ax, drawstyle=self.drawstyle)
            drawn_elements.extend(drawn)
            xpos += elem_length * self.drawstyle.stride
            self._drawn_elements.add(elem)
        ax.autoscale_view()

        return drawn_elements
    
    def legend(
        self, *, 
        ax: Axes, 
        only_drawn: bool=True,
        multi_handle: Literal['first', 'last', 'tuple']='first',
        **legend_kwargs):
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
        handles, labels = self.get_legend_handles_labels(
            only_drawn = only_drawn,
            multi_handle = multi_handle
        )
        legend = ax.legend(
            handles, labels, 
            handler_map={tuple: HandlerTuple(ndivide=None)}, 
            **legend_kwargs
        )
        legend.set_zorder(self.drawstyle.zorder + 1)
        return legend
    
    def get_legend_handles_labels(
        self, 
        *, 
        only_drawn: bool=True,
        multi_handle: Literal['first', 'last', 'tuple']='first'
    ) -> LegendHandlesLabels:
        """
        Return legend handles and labels.

        Parameters
        ----------
        only_drawn : bool, default=True
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
            if only_drawn and elem not in self._drawn_elements:
                continue
            hdl, lbl = artist.get_legend_handle_label(self.drawstyle, multi_handle=multi_handle)
            handles.append(hdl)
            labels.append(lbl)
        return handles, labels
    
    def reset_drawn_elements(self):
        """Reset the set of elements marked as drawn."""
        self._drawn_elements = set()

    def update_drawstyle(self, **changes):
        self._drawstyle = self.drawstyle.with_updates(**changes)

    def to_config(self, file_: Optional[PathOrFile], format_: FileFormat = 'auto'):
        """Write the SecStructArtist configuration to a file."""
        from ..config import SSAConfigWriter
        writer = SSAConfigWriter(self)
        writer.write(file_, format_=format_)

    @classmethod
    def from_config(cls, config_: Union[ArtistKW, PathOrFile], format_: FileFormat = 'auto') -> SecStructArtist:
        """Initializes a SecStructArtist based on a config file"""
        from ..config import SSAConfigReader
        reader = SSAConfigReader(config_, format_=format_)
        return reader.get_secstructartist()