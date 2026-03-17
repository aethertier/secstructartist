import pytest
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path

from secstructartist.artists.primitives.helix import HelixPrimitive, HelixContext


class DummyDrawStyle:
    """Dummy draw style """
    height: float = 2.
    stride: float = 1.5
    linewidth: float = 1.
    linecolor: str = 'red'
    fillcolor: str = '#c0ffee'
    alpha: float = 1.
    zorder: float = 10.

@pytest.fixture
def ds():
    return DummyDrawStyle()


@pytest.fixture
def ax():
    fig, ax = plt.subplots()
    yield ax
    plt.close(fig)

def test_resolve_drawstyle_returns_helixcontext(ds):
    helix = HelixPrimitive()
    ctx = helix.resolve_drawstyle(ds)
    assert isinstance(ctx, HelixContext)

def test_resolve_drawstyle_basic(ds):
    helix = HelixPrimitive(ribbon_period=4.0)
    ctx = helix.resolve_drawstyle(ds, x=0.0, y=0.0, length=8)
    # Inherited fields
    assert ctx.x == 0.0
    assert ctx.y == 0.0
    assert ctx.dx == 8 * ds.stride
    # Helix-specific fields
    expected_halfturns = int(max(1, round(2 * 8 / 4.0)))
    assert ctx.num_halfturns == expected_halfturns
    assert ctx.dx_halfturn == pytest.approx(ctx.dx / expected_halfturns)
    # Default ribbon width (None → 0.5 * period)
    expected_dx_ribbon = 0.5 * 4.0 * ds.stride
    assert ctx.dx_ribbon == pytest.approx(expected_dx_ribbon)
    assert ctx.fill_inner_ribbon is True

def test_resolve_drawstyle_ribbon_width_override(ds):
    helix = HelixPrimitive(ribbon_width=1.2, ribbon_period=4.0)
    ctx = helix.resolve_drawstyle(ds, length=6)
    expected_dx_ribbon = 1.2 * ds.stride
    assert ctx.dx_ribbon == pytest.approx(expected_dx_ribbon)

def test_resolve_drawstyle_minimum_halfturn(ds):
    helix = HelixPrimitive(ribbon_period=100.0)  # very large → would round to 0
    ctx = helix.resolve_drawstyle(ds, length=1)
    assert ctx.num_halfturns == 1
    assert ctx.dx_halfturn == pytest.approx(ctx.dx)  # since only one half-turn

def test_resolve_drawstyle_scaling_and_offsets(ds):
    helix = HelixPrimitive(
        xy_offset=(1.0, -2.0),
        height_scalar=2.0,
        linewidth_scalar=3.0,
        zorder_offset=5.0,
        alpha_scalar=0.5,
    )
    ctx = helix.resolve_drawstyle(ds, x=2.0, y=3.0, length=4)
    # Offsets
    assert ctx.x == 3.0
    assert ctx.y == 1.0
    # Scaling
    assert ctx.dy == pytest.approx(0.5 * ds.height * 2.0)
    assert ctx.linewidth == pytest.approx(ds.linewidth * 3.0)
    assert ctx.zorder == pytest.approx(ds.zorder + 5.0)
    assert ctx.alpha == pytest.approx(ds.alpha * 0.5)

def test_helix_draw_basic(ax, ds):
    helix = HelixPrimitive(
        height_scalar=1.0,
        linewidth_scalar=2.0,
        linecolor="k",
        fillcolor="r",
        zorder_offset=1.0,
    )
    patch = helix.draw(
        x=0.0,
        y=0.0,
        length=10,
        ax=ax,
        drawstyle=ds,
    )
    # Correct type
    assert isinstance(patch, PathPatch)
    # Added to axes
    assert patch in ax.patches
    # Style scaling
    assert patch.get_linewidth() == pytest.approx(ds.linewidth * 2.0)
    assert patch.get_zorder() == pytest.approx(ds.zorder + 1.0)
    # Path integrity
    path = patch.get_path()
    assert isinstance(path, Path)
    assert len(path.vertices) > 0
    assert len(path.codes) == len(path.vertices)
    # Must contain MOVETO codes
    assert Path.MOVETO in path.codes
    assert Path.LINETO in path.codes


def test_legend_handle(ds):
    helix = HelixPrimitive(
        linewidth_scalar=3.0,
        linecolor="b",
        fillcolor="g",
    )
    handle = helix.get_legend_handle(ds)
    assert isinstance(handle, Rectangle)
    assert handle.get_linewidth() == pytest.approx(ds.linewidth * 3.0)
    assert handle.get_edgecolor() is not None
    assert handle.get_facecolor() is not None


def test_to_dict():
    helix = HelixPrimitive(
        ribbon_width=0.8,
        ribbon_period=4.0,
        fill_inner_ribbon=True,
        height_scalar=0.9,
    )
    d = helix.to_dict()
    assert d["ribbon_width"] == 0.8
    assert d["ribbon_period"] == 4.0
    assert d["fill_inner_ribbon"] is True
    assert d["height_scalar"] == 0.9
