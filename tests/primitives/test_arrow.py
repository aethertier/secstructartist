import pytest
import matplotlib.pyplot as plt
from matplotlib.colors import same_color
from matplotlib.patches import Polygon, Rectangle

from secstructartist.artists.primitives import ArrowPrimitive

class DummyDrawStyle:
    """Dummy draw style """
    height: float = 1.
    stride: float = 1.
    linewidth: float = 1.
    zorder: float = 5.


@pytest.fixture
def ds():
    return DummyDrawStyle()


@pytest.fixture
def ax():
    fig, ax = plt.subplots()
    yield ax
    plt.close(fig)


def test_arrow_with_shaft(ax, ds):
    arrow = ArrowPrimitive(
        arrow_tip_length=5.0,
        height_scalar=1.0,
        height_scalar2=0.5,
        linewidth_scalar=2.0,
        linecolor="k",
        fillcolor="r",
        zorder_offset=-.5,
    )
    patch = arrow.draw(x=0, y=0, length=10, ax=ax, drawstyle=ds)
    # TEST: Correct type
    assert isinstance(patch, Polygon)
    # TEST: Correct number of vertices
    assert len(patch.get_xy()) == 8
    # TEST: Filled?
    assert patch.get_fill() is True
    # TEST: Linewidth scaling
    assert patch.get_linewidth() == pytest.approx(ds.linewidth * 2.0)
    # TEST: Zorder
    assert patch.get_zorder() == pytest.approx(ds.zorder - .5)


def test_arrow_without_shaft(ax, ds):
    arrow = ArrowPrimitive(arrow_tip_length=5.)
    patch = arrow.draw(x=0, y=0, length=4, ax=ax, drawstyle=ds)
    # TEST: Correct number of vertices
    assert len(patch.get_xy()) == 4


def test_height_scalar2():
    arrow = ArrowPrimitive(height_scalar=2.)
    # TEST: Default height_scalar2
    assert arrow.height_scalar2 == pytest.approx(0.7 * 2.0)
    # TEST: Override height_scalar2
    arrow.height_scalar2 = 1.8
    assert arrow.height_scalar2 == pytest.approx(1.8)


def test_legend_handle(ds):
    arrow = ArrowPrimitive(arrow_tip_length=5, linecolor='#1f77b4', fillcolor='#aec7e8')
    handle = arrow.get_legend_handle(drawstyle = ds)
    # TEST: Handle
    assert isinstance(handle, Rectangle)
    assert handle.get_width() == pytest.approx(1.)
    assert handle.get_height() == pytest.approx(1.)
    assert same_color(handle.get_edgecolor(), '#1f77b4')
    assert same_color(handle.get_facecolor(), '#aec7e8')


def test_to_dict():
    arrow = ArrowPrimitive(height_scalar=.6, arrow_tip_length=4.)
    d = arrow.to_dict()
    assert 'xy_offset' in d
    assert 'arrow_tip_length' in d
    assert 'height_scalar' in d
    assert 'height_scalar2' in d
    assert d['height_scalar'] == pytest.approx(.6)
    assert d['height_scalar2'] is None
    assert d['arrow_tip_length'] == pytest.approx(4.)
