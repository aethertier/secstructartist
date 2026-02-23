import pytest

from secstructartist.artists.primitives.base import PrimitiveArtist


class DummyPrimitive(PrimitiveArtist):
    def draw(self, *args, **kwargs):
        return None
    def get_legend_handle(self, *args, **kwargs):
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
    assert primitive.linecolor == 'k'
    assert primitive.fillcolor == 'w'


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