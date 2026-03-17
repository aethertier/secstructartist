import pytest
import matplotlib.pyplot as plt
from matplotlib.colors import same_color
from matplotlib.patches import Polygon, Rectangle

from secstructartist.artists.primitives.arrow import ArrowPrimitive, ArrowContext

class DummyDrawStyle:
    """Dummy draw style """
    height: float = 1.
    stride: float = 1.
    linewidth: float = 1.
    linecolor: str = 'red'
    fillcolor: str = '#c0ffee'
    alpha: float = 1.
    zorder: float = 5.


@pytest.fixture
def ds():
    return DummyDrawStyle()


@pytest.fixture
def ax():
    fig, ax = plt.subplots()
    yield ax
    plt.close(fig)


def test_resolve_drawstyle_returns_arrowcontext(ds):
    arrow = ArrowPrimitive()
    ctx = arrow.resolve_drawstyle(ds)
    assert isinstance(ctx, ArrowContext)


def test_resolve_drawstyle_basic(ds):
    arrow = ArrowPrimitive(arrow_tip_length=3.0)
    ctx = arrow.resolve_drawstyle(ds, x=1.0, y=2.0, length=5)
    # Base properties
    assert ctx.x == 1.0
    assert ctx.y == 2.0
    assert ctx.dx == 5 * ds.stride
    # Arrow-specific
    assert ctx.dx_tip == pytest.approx(3.0 * ds.stride)
    assert ctx.dy_tip == pytest.approx(ctx.dy)
    # Default dy_shaft = 0.7 * dy
    assert ctx.dy_shaft == pytest.approx(0.7 * ctx.dy)


def test_resolve_drawstyle_height_scalar2_override(ds):
    arrow = ArrowPrimitive(height_scalar2=0.4)
    ctx = arrow.resolve_drawstyle(ds, length=6)
    expected = 0.5 * ds.height * 0.4
    assert ctx.dy_shaft == pytest.approx(expected)


def test_resolve_drawstyle_scaling_and_offsets(ds):
    arrow = ArrowPrimitive(
        xy_offset=(2.0, -1.0),
        height_scalar=2.0,
        linewidth_scalar=3.0,
        zorder_offset=1.5,
        alpha_scalar=0.25,
        arrow_tip_length=2.0,
    )
    ctx = arrow.resolve_drawstyle(ds, x=1.0, y=1.0, length=4)
    # Offsets
    assert ctx.x == 3.0
    assert ctx.y == 0.0
    # Scaling (inherited)
    assert ctx.dy == pytest.approx(0.5 * ds.height * 2.0)
    assert ctx.linewidth == pytest.approx(ds.linewidth * 3.0)
    assert ctx.zorder == pytest.approx(ds.zorder + 1.5)
    assert ctx.alpha == pytest.approx(ds.alpha * 0.25)
    # Arrow-specific still consistent
    assert ctx.dx_tip == pytest.approx(2.0 * ds.stride)
    assert ctx.dy_tip == pytest.approx(ctx.dy)


def test_resolve_drawstyle_dy_shaft_depends_on_scaled_dy(ds):
    arrow = ArrowPrimitive(height_scalar=2.0)  # affects dy
    ctx = arrow.resolve_drawstyle(ds)
    expected_dy = 0.5 * ds.height * 2.0
    assert ctx.dy == pytest.approx(expected_dy)
    assert ctx.dy_shaft == pytest.approx(0.7 * expected_dy)


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
