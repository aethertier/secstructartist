from __future__ import annotations
from typing import List, Iterable, Tuple, TYPE_CHECKING
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from ..primitives.base import PrimitiveArtist

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from .drawstyle import DrawStyle
    from ..primitives.base import DrawnObj

        
        
        
        # ax.update_datalim(line.get_xydata())
        # ax.autoscale_view()
        # ax.update_datalim(sheet.xy)
        # ax.autoscale_view()
    

class ElementArtist:
    """
    Composite artist for a secondary structure element.

    An ElementArtist represents a contiguous secondary structure element
    (e.g. helix, sheet, or loop) and is responsible for coordinating the
    drawing of one or more :class:`PrimitiveArtist` instances that define
    its visual appearance.
    """
    def __init__(self, primitives: Iterable[PrimitiveArtist]=None, label: str=''):
        """
        Parameters
        ----------
        primitives : iterable of PrimitiveArtist, optional
            Primitive artists used to render the element. Primitives are drawn
            in the order they are provided.

        label : str, optional
            Label used for legend entries.
        """
        self.primitives: List[PrimitiveArtist] = list(primitives) or []
        self.label = label

    def draw(
        self, 
        x: float, y: float, 
        length: int, 
        ax: Axes, 
        drawstyle: DrawStyle
    ) -> List[DrawnObj]:
        """
        Draw a secondary structure element.

        The element is rendered by delegating drawing to all contained
        :class:`PrimitiveArtist` instances.

        Parameters
        ----------
        x : float
            X-coordinate of the first residue.

        y : float
            Y-coordinate of the schematic baseline.

        length : int
            Length of the element in residues.

        ax : matplotlib.axes.Axes
            Axes into which the element is drawn.

        drawstyle : DrawStyle
            Drawing style context used for rendering.

        Returns
        -------
        list
            List of Matplotlib artists created by the primitives.
        """
        drawn = []
        for prim in self.primitives:
            d = prim.draw(x, y, length=length, ax= ax, drawstyle=drawstyle) 
            drawn.append(d)            
        return drawn

    def get_legend_handle_label(self, drawstyle) -> Tuple[Tuple[DrawnObj, ...], str]:
        handle = tuple(
            p.get_legend_handle(drawstyle) for p in self.primitives
        )
        """
        Return legend handle(s) and label for the element.

        The legend handle is constructed by combining the legend handles of
        all contained primitives.

        Parameters
        ----------
        drawstyle : DrawStyle
            Drawing style used to generate legend handles.

        Returns
        -------
        handle : tuple of Matplotlib artists
            Combined legend handle representing the element.

        label : str
            Legend label for the element.
        """
        return handle, self.label
