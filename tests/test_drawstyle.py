import pytest
from secstructartist.artists.drawstyle import DrawStyle

def test_default_values():
    ds = DrawStyle()
    assert ds.height == 1.0
    assert ds.stride == 1.0
    assert ds.linewidth == 1.0
    assert ds.zorder == 5.0

def test_drawstyle_is_frozen():
    ds = DrawStyle()
    with pytest.raises(Exception):
        ds.height = 2.0

def test_with_updates_returns_new_instance():
    ds = DrawStyle()
    new_ds = ds.with_updates(height=2.0)
    assert new_ds is not ds
    assert new_ds.height == 2.0
    assert ds.height == 1.0  # original unchanged

def test_with_multiple_updates():
    ds = DrawStyle()
    new_ds = ds.with_updates(height=2.0, stride=3.0)
    assert new_ds.height == 2.0
    assert new_ds.stride == 3.0
    assert ds.height == 1.0
    assert ds.stride == 1.0

def test_to_dict():
    ds = DrawStyle(height=2.0, stride=3.0, linewidth=4.0, zorder=10.0)
    d = ds.to_dict()
    assert d == {
        "height": 2.0,
        "stride": 3.0,
        "linewidth": 4.0,
        "zorder": 10.0,
    }