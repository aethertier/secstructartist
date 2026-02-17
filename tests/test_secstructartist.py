import pytest
import matplotlib.pyplot as plt
from matplotlib.patches import  Rectangle
from unittest.mock import MagicMock, patch

from secstructartist.artists.secstruct import SecStructArtist, _aggregate
from secstructartist.artists.drawstyle import DrawStyle


@pytest.fixture
def ax():
    fig, ax = plt.subplots()
    yield ax
    plt.close(fig)


@pytest.fixture
def mock_elements():
    elem1 = MagicMock()
    elem2 = MagicMock()
    elem1.draw.return_value = ['c0ffee']
    elem2.draw.return_value = ['bada55']
    h1 = Rectangle(xy=(0,0), width=1, height=1, facecolor='#c0ffee')
    h2 = Rectangle(xy=(0,0), width=1, height=1, facecolor='#bada55')
    elem1.get_legend_handle_label.return_value = (h1, 'C0FFEE')
    elem2.get_legend_handle_label.return_value = (h2, 'BADA55')
    return {'A': elem1, '&': elem2}

# ------------------------------------------------------------------
# Test aggregate function
# ------------------------------------------------------------------

def test_aggregate_basic():
    result = list(_aggregate(">>----aaa"))
    assert result == [(">", 2), ("-", 4), ("a", 3)]

def test_aggregate_single():
    result = list(_aggregate("0"))
    assert result == [("0", 1)]

def test_aggregate_empty():
    result = list(_aggregate([]))
    assert result == []


# ------------------------------------------------------------------
# Test SecStructArtist
# ------------------------------------------------------------------

def test_init_and_repr(mock_elements):
    ssa = SecStructArtist(elements=mock_elements)
    assert ssa.elements == mock_elements
    assert isinstance(ssa.drawstyle, DrawStyle)
    r = repr(ssa)
    assert 'A' in r and '&' in r


def test_draw_calls_elements(mock_elements, ax):
    ssa = SecStructArtist(elements=mock_elements, stride=2.0)
    result = ssa.draw("AAAA&AA", x=0, y=0, ax=ax) 
    # Aggregation: [(A, 4), (&, 1), (A, 2)]
    mock_elements['&'].draw.assert_called_once()
    assert mock_elements['A'].draw.call_count == 2
    # Result flattening
    assert result == ['c0ffee', 'bada55', 'c0ffee']


def test_draw_updates_x_position(mock_elements, ax):
    ssa = SecStructArtist(elements=mock_elements, stride=2.0)
    ssa.draw("&&", x=1, y=0, ax=ax)
    args, kwargs = mock_elements['&'].draw.call_args
    assert args[0] == 1  # x start
    assert kwargs["length"] == 2

def test_draw_missing_element(mock_elements, ax):
    ssa = SecStructArtist(elements=mock_elements)
    with pytest.raises(ValueError):
        ssa.draw("X", ax=ax)

def test_draw_requires_ax(mock_elements):
    ssa = SecStructArtist(elements=mock_elements)
    with pytest.raises(ValueError):
        ssa.draw('AAAA')

def test_drawstyle_update_on_draw(mock_elements, ax):
    ssa = SecStructArtist(elements=mock_elements)
    ssa.draw('AA', ax=ax, stride=3.0)
    assert ssa.drawstyle.stride == 3.0

def test_get_legend_handles_labels_only_drawn(mock_elements, ax):
    ssa = SecStructArtist(elements=mock_elements)
    ssa.draw('&&', ax=ax)
    handles, labels = ssa.get_legend_handles_labels()
    assert isinstance(handles[0], Rectangle)
    assert labels == ['BADA55']

def test_get_legend_handles_labels_all(mock_elements):
    ssa = SecStructArtist(elements=mock_elements)
    handles, labels = ssa.get_legend_handles_labels(only_drawn=False)
    assert all(isinstance(hdl, Rectangle) for hdl in handles)
    assert labels == ["C0FFEE", "BADA55"]

def test_legend_creates_matplotlib_legend(mock_elements, ax):
    ssa = SecStructArtist(elements=mock_elements)
    ssa.draw('AAA', ax=ax)
    legend = ssa.legend(ax=ax)
    assert legend is not None
    assert legend.get_zorder() == pytest.approx(ssa.drawstyle.zorder + 1)

def test_reset_drawn_elements(mock_elements, ax):
    ssa = SecStructArtist(elements=mock_elements)
    ssa.draw('&&', ax=ax)
    assert '&' in ssa._drawn_elements
    ssa.reset_drawn_elements()
    assert ssa._drawn_elements == set()

def test_getattr_forwarding(mock_elements):
    ssa = SecStructArtist(elements=mock_elements, stride=4.0)
    assert ssa.stride == 4.0

def test_getattr_invalid(mock_elements):
    ssa = SecStructArtist(elements=mock_elements)
    with pytest.raises(AttributeError):
        _ = ssa.nonexistent

@patch("secstructartist.io.SSAConfigWriter")
def test_to_config_calls_writer(mock_writer, mock_elements):
    ssa = SecStructArtist(elements=mock_elements)
    instance = mock_writer.return_value
    ssa.to_config("file.json")
    instance.write.assert_called_once()

@patch("secstructartist.io.SSAConfigReader")
def test_from_config_calls_reader(mock_reader):
    reader_instance = mock_reader.return_value
    reader_instance.get_secstructartist.return_value = "SSA"
    result = SecStructArtist.from_config("file.json")
    assert result == "SSA"