import pytest
from unittest.mock import MagicMock
import matplotlib.pyplot as plt

from secstructartist.main import draw_secondary_structure
from secstructartist.artists import SecStructArtist


# ---------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------

@pytest.fixture
def secstruct():
    return "LLHHHLL"

@pytest.fixture
def axis():
    fig, ax = plt.subplots(subplot_kw={"projection": "secstruct"})
    yield ax
    plt.close(fig)


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

def test_creates_new_axis_when_none(secstruct):
    """
    If ax=None, a new secstruct projection axis should be created
    and drawing delegated to ax.draw_secondary_structure.
    """
    result = draw_secondary_structure(secstruct)
    assert result is not None

def test_uses_existing_axis(secstruct, axis, monkeypatch):
    """
    If an axis is provided, artist.draw should be used directly.
    """
    mock_artist = MagicMock(spec=SecStructArtist)
    mock_artist.draw.return_value = ["sentinel"]

    result = draw_secondary_structure(
        secstruct,
        ax=axis,
        artist=mock_artist
    )
    mock_artist.draw.assert_called_once()
    assert result == ["sentinel"]

def test_resolves_artist_from_config(secstruct, axis, monkeypatch):
    """
    If artist is not a SecStructArtist instance,
    SecStructArtist.from_config must be used.
    """
    mock_artist = MagicMock(spec=SecStructArtist)
    mock_artist.draw.return_value = ["ok"]

    def fake_from_config(config):
        return mock_artist
    
    monkeypatch.setattr(
        SecStructArtist,
        "from_config",
        staticmethod(fake_from_config)
    )
    result = draw_secondary_structure(
        secstruct,
        ax=axis,
        artist="default"
    )
    assert result == ["ok"]
    mock_artist.draw.assert_called_once()

def test_does_not_reresolve_artist_instance(secstruct, axis, monkeypatch):
    """
    If artist already is SecStructArtist,
    from_config must NOT be called.
    """
    mock_artist = MagicMock(spec=SecStructArtist)
    mock_artist.draw.return_value = ["ok"]

    spy = MagicMock()
    monkeypatch.setattr(SecStructArtist, "from_config", spy)

    draw_secondary_structure(
        secstruct,
        ax=axis,
        artist=mock_artist
    )

    spy.assert_not_called()
    mock_artist.draw.assert_called_once()

def test_forwards_drawstyle_kwargs(secstruct, axis):
    """
    Additional kwargs must be forwarded to artist.draw.
    """
    mock_artist = MagicMock(spec=SecStructArtist)
    mock_artist.draw.return_value = ["styled"]

    draw_secondary_structure(
        secstruct,
        ax=axis,
        artist=mock_artist,
        height = 42,
        linewidth = .42,
    )

    mock_artist.draw.assert_called_once()

    _, kwargs = mock_artist.draw.call_args
    assert kwargs["height"] == 42
    assert pytest.approx(kwargs["linewidth"]) == .42