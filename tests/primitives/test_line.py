import pytest
import matplotlib.pyplot as plt
from matplotlib.colors import same_color
from matplotlib.lines import Line2D

from secstructartist.artists.primitives import LinePrimitive


class DummyDrawStyle:
    """Dummy draw style."""
    height: float = 1.0
    stride: float = 2.0
    linewidth: float = 1.5
    zorder: float = 5.0


@pytest.fixture
def ds():
    return DummyDrawStyle()


@pytest.fixture
def ax():
    fig, ax = plt.subplots()
    yield ax
    plt.close(fig)


def test_line_draw(ax, ds, length=3):
    line_primitive = LinePrimitive(
        linewidth_scalar=2.0,
        linecolor='#C0FFEE',
    )
    line = line_primitive.draw(
        x=.5, y=2.0, length=length, ax=ax, drawstyle=ds,
    )
    # TEST: Correct type
    assert isinstance(line, Line2D)
    # TEST: Line added to axes
    assert line in ax.lines
    # TEST: Correct coordinates
    xdata, ydata = line.get_data()
    assert xdata[0] == pytest.approx(.5)
    assert xdata[1] == pytest.approx(.5 + ds.stride * length)
    assert ydata[0] == pytest.approx(2.)
    assert ydata[1] == pytest.approx(2.)
    # TEST: Linewidth scaling
    assert line.get_linewidth() == pytest.approx(ds.linewidth * 2.0)
    # TEST: Color
    assert same_color(line.get_color(), '#C0FFEE')
    # TEST: Zorder (line specific offset defaults: -0.1)
    assert line.get_zorder() == pytest.approx(ds.zorder - 0.1)


def test_line_draw_zorder_override(ax, ds, length=4):   
    line_primitive = LinePrimitive(zorder_offset=3.)
    line = line_primitive.draw(
        x=1.0, y=1.0, length=length, ax=ax, drawstyle=ds,
    )
    # TEST: Line added to axes
    assert line in ax.lines
    # TEST: Zorder (line specific offset defaults: -0.1)
    assert line.get_zorder() == pytest.approx(ds.zorder + 3.)


def test_legend_handle(ds):
    line_primitive = LinePrimitive(
        linewidth_scalar=3.0,
        linecolor='coral',
    )
    handle = line_primitive.get_legend_handle(ds)
    # TEST: Handle
    assert isinstance(handle, Line2D)
    assert handle.get_linewidth() == pytest.approx(ds.linewidth * 3.0)
    assert same_color(handle.get_color(), 'coral')
    # TEST: Correct default coordinates
    xdata, ydata = handle.get_data()
    assert xdata == [0.0, 1.0]
    assert ydata == [0.5, 0.5]


def test_to_dict():
    line_primitive = LinePrimitive(
        xy_offset=(1.0, 2.0),
        height_scalar=0.8,
        linewidth_scalar=1.5,
        linecolor="#bada55",
        zorder_offset=2.0,
    )
    d = line_primitive.to_dict()
    # Ensure base parameters are present
    assert "xy_offset" in d
    assert "height_scalar" in d
    assert "linewidth_scalar" in d
    assert "linecolor" in d
    assert "zorder_offset" in d
    assert d["xy_offset"] == [1.0, 2.0]
    assert d["height_scalar"] == pytest.approx(0.8)
    assert d["linewidth_scalar"] == pytest.approx(1.5)
    assert d["linecolor"] == "#bada55"
    assert d["zorder_offset"] == pytest.approx(2.0)
