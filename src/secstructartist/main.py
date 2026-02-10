from __future__ import annotations
from typing import Any, Iterable, Optional, Union, TYPE_CHECKING
from matplotlib.axes import Axes
from matplotlib.pyplot import subplots
from .artists import SecStructArtist

if TYPE_CHECKING:
    from .typing_ import ArtistConfig


def draw_secondary_structure(
    secstruct: Iterable[str] | str,
    x: float = 1., 
    y: float = 1., 
    *,
    ax: Optional[Axes] = None,
    artist: Union[ArtistConfig, SecStructArtist] = 'default',
    **drawstyle_kwargs: Optional[Any]
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
        should be present in the self.elements dictionary.

    x : float
        The position of the first residue in the x-axis. (default: 1.)

    y : float
        The position of the first residue in the y-axis. (default: 1.)

    ax : Axes
        :class:`Axes` object where the secondary structure scheme is drawn. 
        If None, a new figure will be generated.

    artist : {'default', 'dssp', Path, SecStructArtist}
        The artist used to draw the secondary structure. This could be a string
        with 'default' or 'dssp' to use either of those predefined settings.
        This could be aa path to a config file from which the settings will
        be read, or this could be a SecStructArtist object.
    
    **drawstyle_kwargs : dict, optional
        Additional keyword arguments passed to the artist during
        initialization or configuration. These arguments override
        settings defined by the selected artist or configuration file.
    """
    # Get the artist to be used for drawing
    if not isinstance(artist, SecStructArtist):
        artist = SecStructArtist.from_config(artist)
    if ax is None:
        n = len(secstruct)
        fig, ax = subplots(figsize=(.05*n, .75), subplot_kw={'projection': 'secstruct'})
    return artist.draw(secstruct, x, y, ax=ax)