from __future__ import annotations
import abc
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple
from ..drawstyle import DrawStyle
from ...typing_ import ColorType, DrawnArtist

if TYPE_CHECKING:
    from matplotlib.axes import Axes


@dataclass(slots=True)
class DrawContext:
    """Context for primitives' ``_draw`` method"""
    x_left: float
    x_right: float
    y_center: float
    height: float
    linewidth: float
    linecolor: ColorType
    fillcolor: ColorType
    zorder: float


class PrimitiveArtist(abc.ABC):
    """
    Abstract base class for graphical drawing primitives.

    A PrimitiveArtist implements the low-level drawing logic for a specific
    graphical shape (e.g. line, arrow, or polygon). Primitives are combined
    by :class:`ElementArtist` instances to form complete secondary structure
    elements.
    """
    def __init__(
        self,
        *,
        xy_offset: Tuple[float, float] = None,
        height_scalar: float = 1.,
        linewidth_scalar: float = 1.,
        zorder_offset: float = 0.,
        linecolor: Optional[ColorType] = None,
        fillcolor: Optional[ColorType] = None,
    ):
        """
        Parameters
        ----------
        xy_offset : tuple of float, optional
            Horizontal and vertical offset applied to the primitive relative
            to the element origin.

        height_scalar : float, default=1.0
            Multiplier applied to the element height.

        linewidth_scalar : float, default=1.0
            Multiplier applied to the base line width.

        zorder_offset : float, default=1
            Offset added to the base z-order.

        linecolor : ColorType, default='k'
            Color used for drawing primitive outlines.

        fillcolor : ColorType or None, default='w'
            Fill color used for closed primitives. If None, the primitive is
            not filled.
        """
        self.x_offset, self.y_offset = (0, 0) if xy_offset is None else xy_offset
        self.height_scalar = height_scalar
        self.linewidth_scalar = linewidth_scalar
        self.zorder_offset = zorder_offset
        self.linecolor = linecolor
        self.fillcolor = fillcolor

    @staticmethod
    @abc.abstractmethod
    def _draw(ctx: DrawContext, ax: Axes) -> DrawnArtist:
        pass

    @staticmethod
    @abc.abstractmethod
    def _get_legend_handle(ctx: DrawContext) -> DrawnArtist:
        pass

    def resolve_drawstyle(self, drawstyle: DrawStyle, x: float=1, y: float=1, length: int=1) -> DrawContext:
        x_left = x + self.x_offset
        x_right = x_left + length * drawstyle.stride
        return DrawContext(
            x_left = x_left,
            x_right = x_right,
            y_center = y + self.y_offset,
            height = drawstyle.height * self.height_scalar,
            linewidth = drawstyle.linewidth * self.linewidth_scalar,
            linecolor = self.linecolor or drawstyle.linecolor,
            fillcolor = self.fillcolor or drawstyle.fillcolor,
            zorder = drawstyle.zorder + self.zorder_offset,
        )

    def draw(self, x: float, y: float, length: int, ax: Axes, drawstyle: DrawStyle) -> DrawnArtist:
        """
        Draw the primitive.

        Parameters
        ----------
        x : float
            X-coordinate of the element origin.

        y : float
            Y-coordinate of the element origin.

        length : int
            Length of the element in residues.

        ax : matplotlib.axes.Axes
            Axes into which the primitive is drawn.

        drawstyle : DrawStyle
            Drawing style context used for rendering.

        Returns
        -------
        DrawnObj
            Matplotlib artist created by the primitive.
        """
        ctx = self.resolve_drawstyle(drawstyle, x, y, length)
        return self._draw(ctx, ax=ax)

    def get_legend_handle(self, drawstyle: DrawStyle) -> DrawnArtist:
        """
        Create a legend handle for the primitive.

        Parameters
        ----------
        drawstyle : DrawStyle
            Drawing style used to generate the legend handle.

        Returns
        -------
        DrawnObj
            Matplotlib artist suitable for use as a legend handle.
        """
        ctx = self.resolve_drawstyle(drawstyle)
        return self._get_legend_handle(ctx)

    def to_dict(self, **additional_atributes) -> Dict[str, Any]:
        selfdict = {
            'type': type(self).__name__,
            'xy_offset': [self.x_offset, self.y_offset],
            'height_scalar': self.height_scalar,
            'linewidth_scalar': self.linewidth_scalar,
            'zorder_offset': self.zorder_offset,
            'linecolor': self.linecolor,
            'fillcolor': self.fillcolor,
        }
        selfdict.update(additional_atributes)
        return selfdict