import pytest
from unittest.mock import MagicMock
from secstructartist.artists.element import ElementArtist


class DummyDrawStyle:
    pass


@pytest.fixture
def ds():
    return DummyDrawStyle()


@pytest.fixture
def mock_primitives():
    prim1 = MagicMock()
    prim1.draw.return_value = "drawn1"
    prim1.get_legend_handle.return_value = "handle1"
    prim2 = MagicMock()
    prim2.draw.return_value = "drawn2"
    prim2.get_legend_handle.return_value = "handle2"
    return prim1, prim2


def test_draw_calls_all_primitives(mock_primitives, ds):
    prim1, prim2 = mock_primitives
    element = ElementArtist(primitives=[prim1, prim2], label="X")
    result = element.draw(
        x=1.0,
        y=2.0,
        length=5,
        ax="ax",
        drawstyle=ds,
    )
    # Correct delegation
    prim1.draw.assert_called_once_with(1.0, 2.0, length=5, ax="ax", drawstyle=ds)
    prim2.draw.assert_called_once_with(1.0, 2.0, length=5, ax="ax", drawstyle=ds)
    # Order preserved
    assert result == ["drawn1", "drawn2"]


def test_draw_empty_primitives(ds):
    element = ElementArtist(primitives=[], label="0")
    result = element.draw(0, 0, 3, ax="ax", drawstyle=ds)
    assert result == []


def test_legend_first(mock_primitives, ds):
    prim1, prim2 = mock_primitives
    element = ElementArtist(primitives=[prim1, prim2], label="F")
    handle, label = element.get_legend_handle_label(ds, multi_handle="first")
    assert handle == "handle1"
    assert label == "F"
    prim1.get_legend_handle.assert_called_once_with(ds)

def test_legend_last(mock_primitives, ds):
    prim1, prim2 = mock_primitives
    element = ElementArtist(primitives=[prim1, prim2], label="L")
    handle, label = element.get_legend_handle_label(ds, multi_handle="last")
    assert handle == "handle2"
    assert label == "L"
    prim2.get_legend_handle.assert_called_once_with(ds)

def test_legend_tuple(mock_primitives, ds):
    prim1, prim2 = mock_primitives
    element = ElementArtist(primitives=[prim1, prim2], label="T")
    handle, label = element.get_legend_handle_label(ds, multi_handle="tuple")
    assert handle == ("handle1", "handle2")
    assert label == "T"

def test_legend_invalid_option(mock_primitives, ds):
    prim1, prim2 = mock_primitives
    element = ElementArtist(primitives=[prim1, prim2], label="W")
    with pytest.raises(ValueError):
        element.get_legend_handle_label(ds, multi_handle="invalid")