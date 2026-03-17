import pytest

from secstructartist.artists.primitives.base import PrimitiveArtist


class DummyDrawStyle:
    """Dummy draw style """
    height: float = 2.
    stride: float = 1.5
    linewidth: float = 1.
    linecolor: str = 'red'
    fillcolor: str = '#c0ffee'
    alpha: float = 1.
    zorder: float = 10.


class DummyPrimitive(PrimitiveArtist):
    @staticmethod
    def _draw(*args, **kwargs):
        return None
    @staticmethod
    def _get_legend_handle(*args, **kwargs):
        return None
    

def test_cannot_instantiate_abstract_class():
    with pytest.raises(TypeError):
        PrimitiveArtist()


def test_default_initialization():
    primitive = DummyPrimitive()
    assert primitive.x_offset == 0
    assert primitive.y_offset == 0
    assert primitive.height_scalar == 1.0
    assert primitive.linewidth_scalar == 1.0
    assert primitive.zorder_offset == 0.0
    assert primitive.linecolor is None
    assert primitive.fillcolor is None


def test_custom_initialization():
    primitive = DummyPrimitive(
        xy_offset=(1.5, -2.0),
        height_scalar=0.5,
        linewidth_scalar=2.0,
        zorder_offset=3.0,
        linecolor='r',
        fillcolor='b',
    )
    assert primitive.x_offset == 1.5
    assert primitive.y_offset == -2.0
    assert primitive.height_scalar == 0.5
    assert primitive.linewidth_scalar == 2.0
    assert primitive.zorder_offset == 3.0
    assert primitive.linecolor == 'r'
    assert primitive.fillcolor == 'b'

def test_to_dict_contains_base_fields():
    primitive = DummyPrimitive(
        xy_offset=(1.0, 2.0),
        height_scalar=0.8,
        linewidth_scalar=1.5,
        zorder_offset=2.0,
        linecolor='#bada55',
        fillcolor=None,
    )
    d = primitive.to_dict()
    assert d['type'] == 'DummyPrimitive'
    assert d['xy_offset'] == [1.0, 2.0]
    assert d['height_scalar'] == 0.8
    assert d['linewidth_scalar'] == 1.5
    assert d['zorder_offset'] == 2.0
    assert d['linecolor'] == '#bada55'
    assert d['fillcolor'] is None


def test_resolve_drawstyle_defaults():
    primitive = DummyPrimitive()
    drawstyle = DummyDrawStyle()
    ctx = primitive.resolve_drawstyle(drawstyle, x=1.0, y=2.0, length=3)
    assert ctx.x == 1.0
    assert ctx.y == 2.0
    assert ctx.dx == 3 * drawstyle.stride
    assert ctx.dy == 0.5 * drawstyle.height
    assert ctx.linewidth == drawstyle.linewidth
    assert ctx.linecolor == drawstyle.linecolor
    assert ctx.fillcolor == drawstyle.fillcolor
    assert ctx.zorder == drawstyle.zorder
    assert ctx.alpha == drawstyle.alpha


def test_resolve_drawstyle_with_offsets_and_scalars():
    primitive = DummyPrimitive(
        xy_offset=(1.0, -1.0),
        height_scalar=2.0,
        linewidth_scalar=3.0,
        zorder_offset=4.0,
        alpha_scalar=0.5,
    )
    drawstyle = DummyDrawStyle()
    ctx = primitive.resolve_drawstyle(drawstyle, x=0.0, y=0.0, length=2)
    assert ctx.x == pytest.approx(1.0)  # offset applied
    assert ctx.y == pytest.approx(-1.0)
    assert ctx.dx == pytest.approx(2 * drawstyle.stride)
    assert ctx.dy == pytest.approx(0.5 * drawstyle.height * 2.0)
    assert ctx.linewidth == pytest.approx(drawstyle.linewidth * 3.0)
    assert ctx.zorder == pytest.approx(drawstyle.zorder + 4.0)
    assert ctx.alpha == pytest.approx(drawstyle.alpha * 0.5)