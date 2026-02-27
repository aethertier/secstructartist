import pytest
import logging
import warnings
from unittest.mock import MagicMock
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.projections import get_projection_class

from secstructartist.axes import SecStructAxes
from secstructartist.artists import SecStructArtist


# ---------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------

@pytest.fixture
def ax():
    fig, ax = plt.subplots(subplot_kw={"projection": "secstruct"})
    yield ax
    plt.close(fig)

@pytest.fixture
def secstruct():
    return "LLHHH"


# ---------------------------------------------------------------------
# Projection Registration
# ---------------------------------------------------------------------

def test_projection_registered():
    """
    The 'secstruct' projection must be registered with matplotlib.
    """
    cls = get_projection_class("secstruct")
    assert cls is SecStructAxes

def test_subplot_creates_secstruct_axes():
    fig, ax = plt.subplots(subplot_kw={"projection": "secstruct"})
    try:
        assert isinstance(ax, SecStructAxes)
    finally:
        plt.close(fig)


# ---------------------------------------------------------------------
# draw_secondary_structure
# ---------------------------------------------------------------------

def test_draw_resolves_artist_from_config(ax, secstruct, monkeypatch):
    """
    If artist is not SecStructArtist, from_config must be called.
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

    result = ax.draw_secondary_structure(secstruct, artist="default")

    assert result == ["ok"]
    mock_artist.draw.assert_called_once()
    assert ax._ssa_secstructartist is mock_artist

def test_draw_uses_existing_artist_instance(ax, secstruct, monkeypatch):
    """
    If artist already is SecStructArtist,
    from_config must NOT be called.
    """
    mock_artist = MagicMock(spec=SecStructArtist)
    mock_artist.draw.return_value = ["drawn"]

    spy = MagicMock()
    monkeypatch.setattr(SecStructArtist, "from_config", spy)

    result = ax.draw_secondary_structure(secstruct, artist=mock_artist)

    assert result == ["drawn"]
    spy.assert_not_called()
    mock_artist.draw.assert_called_once()
    assert ax._ssa_secstructartist is mock_artist

def test_draw_forwards_kwargs(ax, secstruct):
    """
    drawstyle_kwargs must be forwarded to artist.draw.
    """
    mock_artist = MagicMock(spec=SecStructArtist)
    mock_artist.draw.return_value = []

    ax.draw_secondary_structure(
        secstruct,
        artist=mock_artist,
        height = 42,
        linewidth = .42,
    )

    _, kwargs = mock_artist.draw.call_args
    assert kwargs["height"] == 42
    assert pytest.approx(kwargs["linewidth"]) == .42


# ---------------------------------------------------------------------
# legend behavior
# ---------------------------------------------------------------------

def test_legend_falls_back_if_no_artist(ax, caplog, recwarn):
    """
    If no SecStructArtist has been used,
    legend should fall back to matplotlib base legend.
    """
    caplog.set_level(logging.WARNING)
    leg = ax.legend()

    warning_messages = [
        *(str(w.message) for w in recwarn),
        *(r.getMessage() for r in caplog.records)
    ]
    assert any("No artists with labels found" in msg for msg in warning_messages)
    assert leg is not None

def test_legend_falls_back_if_handles_provided(ax):
    """
    If handles are explicitly provided, fallback must occur.
    """
    handle = Line2D([0],[0])
    leg = ax.legend([handle], ["label"])
    assert leg is not None

def test_legend_delegates_to_artist(ax, secstruct):
    """
    If no explicit handles and artist exists,
    legend must delegate to artist.legend().
    """
    mock_artist = MagicMock(spec=SecStructArtist)
    mock_legend = MagicMock()
    mock_artist.draw.return_value = []
    mock_artist.legend.return_value = mock_legend

    ax.draw_secondary_structure(secstruct, artist=mock_artist)

    result = ax.legend()

    mock_artist.legend.assert_called_once()
    assert result is mock_legend

def test_legend_passes_parameters(ax, secstruct):
    """
    only_drawn and multi_handle must be forwarded correctly.
    """
    mock_artist = MagicMock(spec=SecStructArtist)
    mock_artist.draw.return_value = []
    mock_artist.legend.return_value = MagicMock()

    ax.draw_secondary_structure(secstruct, artist=mock_artist)

    ax.legend(only_drawn=False, multi_handle="tuple")

    _, kwargs = mock_artist.legend.call_args
    assert kwargs["only_drawn"] is False
    assert kwargs["multi_handle"] == "tuple"


# ---------------------------------------------------------------------
# clear()
# ---------------------------------------------------------------------

def test_clear_resets_artist(ax, secstruct):
    """
    After clear(), the associated SecStructArtist must be removed.
    """
    mock_artist = MagicMock(spec=SecStructArtist)
    mock_artist.draw.return_value = []

    ax.draw_secondary_structure(secstruct, artist=mock_artist)
    assert ax._ssa_secstructartist is mock_artist

    ax.clear()

    assert ax._ssa_secstructartist is None