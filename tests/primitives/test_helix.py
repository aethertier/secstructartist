import pytest
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path

from secstructartist.artists.primitives import HelixPrimitive


class DummyDrawStyle:
    height: float = 2.0
    stride: float = 1.5
    linewidth: float = 1.0
    zorder: float = 10.0


@pytest.fixture
def ds():
    return DummyDrawStyle()


@pytest.fixture
def ax():
    fig, ax = plt.subplots()
    yield ax
    plt.close(fig)


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


def test_pathgen_codes_valid():
    helix = HelixPrimitive()
    verts = [
        [[0, 0], [1, 0], [1, 1]],
        [[2, 0], [3, 0], [3, 1]],
    ]
    codes = helix._pathgen_codes(verts)
    # Each segment must begin with MOVETO
    assert codes[0] == Path.MOVETO
    assert Path.LINETO in codes


def test_pathgen_codes_invalid():
    helix = HelixPrimitive()
    verts = [[[0, 0], [1, 0]]]  # only 2 points
    with pytest.raises(ValueError):
        helix._pathgen_codes(verts)


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