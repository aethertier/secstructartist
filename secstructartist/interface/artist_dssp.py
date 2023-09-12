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
    
    def __init__(self, height=1., linewidth=1., zorder=10, 
                    G_kwargs=None, H_kwargs=None, I_kwargs=None, E_kwargs=None,
                    B_kwargs=None, S_kwargs=None, T_kwargs=None, C_Kwargs=None):
        self.height = height
        self.linewidth = linewidth
        self.zorder = zorder
        self._artists = {}
        self["G"] = art.HelixArtist(**(G_kwargs or {})) 
        self["H"] = art.HelixArtist(**(H_kwargs or {})) 
        self["I"] = art.HelixArtist(**(I_kwargs or {}))
        self["E"] = art.SheetArtist(**(E_kwargs or {}))
        self["B"] = art.SheetArtist(**(B_kwargs or {}))
        self["S"] = art.LoopArtist(**(S_kwargs or {}))
        self["T"] = art.LoopArtist(**(T_kwargs or {}))
        self["C"] = art.LoopArtist(**(C_Kwargs or {}))
        self["c"] =  self["C"]
        self[" "] =  self["C"]