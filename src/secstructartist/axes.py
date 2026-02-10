from __future__ import annotations
from typing import Any, Iterable, List, Literal, Optional, Union, TYPE_CHECKING
from matplotlib.axes import Axes
from matplotlib.projections import register_projection
from .artists import SecStructArtist

if TYPE_CHECKING:
    from matplotlib.legend import Legend
    from .typing_ import ArtistConfig, DrawnArtist

class SecStructAxes(Axes):
    """
    Matplotlib Axes subclass for drawing secondary-structure schematics.

    This projection integrates :class:`SecStructArtist` and provides
    convenience methods for rendering secondary structure annotations
    and generating corresponding legends.
    """
    name = "secstruct"   # this is the projection name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ssa_secstructartist: Optional[SecStructArtist] = None

    def draw_secondary_structure(
        self,
        secstruct: Iterable[str] | str,
        x: float = 1., 
        y: float = 1., *,
        artist: Union[ArtistConfig, SecStructArtist] = 'default',
        **drawstyle_kwargs: Optional[Any]
    ) -> List[DrawnArtist]:
        """
        Draw a secondary-structure schematic into the axes.

        Consecutive residues with identical secondary-structure labels
        are grouped and rendered as a single continuous graphical element.

        Parameters
        ----------
        secstruct : str or Iterable[str]
            Residue-wise secondary-structure labels.

        x, y : float
            Position of the first residue. Defaults to (1., 1.).

        artist : {'default', 'dssp', Path, SecStructArtist}
            Artist or configuration used to render the structure.

        **drawstyle_kwargs
            Keyword arguments overriding artist or configuration defaults.

        Returns
        -------
        Any
            Artists created by the underlying :class:`SecStructArtist`.
        """
        if not isinstance(artist, SecStructArtist):
            artist = SecStructArtist.from_config(artist)
        self._ssa_secstructartist = artist
        drawn = artist.draw(secstruct, x=x, y=y, ax=self, **drawstyle_kwargs)
        return drawn
    
    def legend(self, 
        *args, 
        only_drawn: bool = True, 
        multi_handle:  Literal['first', 'last', 'tuple'] = 'first',
        **kwargs
    ) -> Legend:
        """
        Create a legend for the secondary-structure schematic.

        If legend handles are explicitly provided, or no secondary-structure
        artist is associated with the axes, this falls back to the base
        Matplotlib legend behavior.

        Parameters
        ----------
        only_drawn : bool, default=True
            If True, return handles only for elements that have been drawn.

        multi_handle : Literal['first', 'last', 'tuple'], default='first'
            If an ElementArtist produces multiple handles, determine which handle
            is displayed. If ``'tuple'`` is provided, all handles are displayed
            alongside each other.

        **kwargs
            These correspond to ``matplotlib.pyplot.legend`` keywords.
        """
        artist = self._ssa_secstructartist
        # IF handles are explicitely provided or there is no SecStructArtist
        if args or 'handles' in kwargs or artist is None:
            return super().legend(*args, **kwargs)
        
        # ELSE Get secondary structure artist legend handles.
        legend = artist.legend(
            ax = self,
            only_drawn = only_drawn,
            multi_handle = multi_handle,
            **kwargs
        )
        return legend

    def clear(self):
        super().clear()
        self._ssa_secstructartist = None

register_projection(SecStructAxes)
