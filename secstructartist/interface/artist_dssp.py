"""A special artist designed to work with the structure codes of DSSP"""
from .artist import SecStructArtist
from .. import artists as art


class SecStructArtistDssp(SecStructArtist):
    """Class to draw secondary structure representations

    All secondary structure representations are typically drawn in an existing
    maplotlib axis.

    Attributes:
    -----------
        height : float
            Height of the secondary structure elements to be drawn in y-axis 
            scale (default: 1.)
        linewidth : float
            Linewidth of the secondary structure elements to be drawn (default: 1.)
        zorder : float
            Corresponds to the zorder argument of matplotlib. Elements are draw
            in the range [zorder-.5, zorder] to handle internal overlays. 
            (default: 10.)
        artists : dict
            Dictionary where the keys correspond to secondary structure codes,
            and the values are the artists used to visualize the corresponding
            secondary structure. This is fully customizable with artists from 
            the `.artists` submodule. By default the following artists are 
            initialized:
                "H  -> HelixArtist
                "G" -> HelixArtist
                "I" -> HelixArtist
                "E" -> SheetArtist
                "B" -> SheetArtist
                "S" -> LoopArtist
                "T" -> LoopArtist
                {"c", "C", " "} -> LoopArtist

    Methods:
    --------
        draw(secstruct, xpos, ypos, ax) -> (Figure, List[DrawnSecStructElement])
            Draws the secondary structure given by secstruct, and returns a 
            list of all the objects drawn.
    """
    
    def __init__(self, height=1., linewidth=1., zorder=10,  helix_kwargs=None, 
                    loop_kwargs=None, sheet_kwargs=None):
        self.height = height
        self.linewidth = linewidth
        self.zorder = zorder
        loop = art.LoopArtist(self, **(loop_kwargs or {}))
        self.artists = {
            "G": art.HelixArtist(self, **(helix_kwargs or {})), 
            "H": art.HelixArtist(self, **(helix_kwargs or {})), 
            "I": art.HelixArtist(self, **(helix_kwargs or {})),
            "E": art.SheetArtist(self, **(sheet_kwargs or {})),
            "B": art.SheetArtist(self, **(sheet_kwargs or {})),
            "S": art.LoopArtist(self, **(loop_kwargs or {})),
            "T": art.LoopArtist(self, **(loop_kwargs or {})),
            "c": loop, "C": loop, " ": loop
        }