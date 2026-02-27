import pytest
from unittest.mock import MagicMock

from secstructartist.config import SSAConfigReader


# ---------------------------------------------------------------------
# Minimal Test Configuration
# ---------------------------------------------------------------------

@pytest.fixture
def minimal_config():
    return {
        "drawstyle": {"linewidth": 2},
        "primitives": {
            "circle-001": {"type": "circle", "radius": 3},
        },
        "elements": {
            "H": {
                "label": "helix",
                "primitives": ["circle-001"],
            }
        },
    }


# ---------------------------------------------------------------------
# Initialization / load_configuration
# ---------------------------------------------------------------------

def test_load_configuration_called(monkeypatch, minimal_config):
    spy = MagicMock(return_value=minimal_config)

    monkeypatch.setattr(
        "secstructartist.config.configreader.load_configuration",
        spy
    )

    SSAConfigReader("dummy.json")

    spy.assert_called_once()


# ---------------------------------------------------------------------
# config property
# ---------------------------------------------------------------------

def test_config_property_raises_if_none():
    reader = SSAConfigReader.__new__(SSAConfigReader)
    reader._config = None

    with pytest.raises(RuntimeError):
        _ = reader.config


# ---------------------------------------------------------------------
# Primitive Parsing
# ---------------------------------------------------------------------

def test_get_primitiveartists(monkeypatch, minimal_config):
    monkeypatch.setattr(
        "secstructartist.config.configreader.load_configuration",
        lambda *_: minimal_config
    )

    mock_primitive_class = MagicMock()
    mock_instance = MagicMock()
    mock_primitive_class.return_value = mock_instance

    monkeypatch.setattr(
        "secstructartist.config.configreader.PRIMITIVES_AVAIL",
        {"circle": mock_primitive_class}
    )

    reader = SSAConfigReader("dummy")

    primitives = reader.get_primitiveartists()

    assert "circle-001" in primitives
    mock_primitive_class.assert_called_once_with(radius=3)


def test_get_primitiveartists_cached(monkeypatch, minimal_config):
    monkeypatch.setattr(
        "secstructartist.config.configreader.load_configuration",
        lambda *_: minimal_config
    )

    mock_primitive_class = MagicMock()
    monkeypatch.setattr(
        "secstructartist.config.configreader.PRIMITIVES_AVAIL",
        {"circle": mock_primitive_class}
    )

    reader = SSAConfigReader("dummy")

    p1 = reader.get_primitiveartists()
    p2 = reader.get_primitiveartists()

    assert p1 is p2
    mock_primitive_class.assert_called_once()


# ---------------------------------------------------------------------
# Element Parsing
# ---------------------------------------------------------------------

def test_get_elementartists(monkeypatch, minimal_config):
    monkeypatch.setattr(
        "secstructartist.config.configreader.load_configuration",
        lambda *_: minimal_config
    )

    # Mock primitive creation
    mock_primitive_instance = MagicMock()
    monkeypatch.setattr(
        "secstructartist.config.configreader.PRIMITIVES_AVAIL",
        {"circle": lambda **kwargs: mock_primitive_instance}
    )

    mock_element_class = MagicMock()
    mock_element_instance = MagicMock()
    mock_element_class.return_value = mock_element_instance

    monkeypatch.setattr(
        "secstructartist.config.configreader.ElementArtist",
        mock_element_class
    )

    reader = SSAConfigReader("dummy")

    elements = reader.get_elementartists()

    assert "H" in elements
    mock_element_class.assert_called_once()
    _, kwargs = mock_element_class.call_args
    assert kwargs["label"] == "helix"


def test_get_elementartists_cached(monkeypatch, minimal_config):
    monkeypatch.setattr(
        "secstructartist.config.configreader.load_configuration",
        lambda *_: minimal_config
    )

    monkeypatch.setattr(
        "secstructartist.config.configreader.PRIMITIVES_AVAIL",
        {"circle": lambda **kwargs: MagicMock()}
    )

    monkeypatch.setattr(
        "secstructartist.config.configreader.ElementArtist",
        MagicMock()
    )

    reader = SSAConfigReader("dummy")

    e1 = reader.get_elementartists()
    e2 = reader.get_elementartists()

    assert e1 is e2


# ---------------------------------------------------------------------
# Drawstyle
# ---------------------------------------------------------------------

def test_get_drawstyle(monkeypatch, minimal_config):
    monkeypatch.setattr(
        "secstructartist.config.configreader.load_configuration",
        lambda *_: minimal_config
    )

    reader = SSAConfigReader("dummy")

    drawstyle = reader.get_drawstyle()

    assert drawstyle == {"linewidth": 2}


def test_get_drawstyle_cached(monkeypatch, minimal_config):
    monkeypatch.setattr(
        "secstructartist.config.configreader.load_configuration",
        lambda *_: minimal_config
    )

    reader = SSAConfigReader("dummy")

    d1 = reader.get_drawstyle()
    d2 = reader.get_drawstyle()

    assert d1 is d2


# ---------------------------------------------------------------------
# SecStructArtist Construction
# ---------------------------------------------------------------------

def test_get_secstructartist(monkeypatch, minimal_config):
    monkeypatch.setattr(
        "secstructartist.config.configreader.load_configuration",
        lambda *_: minimal_config
    )

    monkeypatch.setattr(
        "secstructartist.config.configreader.PRIMITIVES_AVAIL",
        {"circle": lambda **kwargs: MagicMock()}
    )

    monkeypatch.setattr(
        "secstructartist.config.configreader.ElementArtist",
        lambda **kwargs: MagicMock()
    )

    mock_ssa_class = MagicMock()
    mock_ssa_instance = MagicMock()
    mock_ssa_class.return_value = mock_ssa_instance

    monkeypatch.setattr(
        "secstructartist.config.configreader.SecStructArtist",
        mock_ssa_class
    )

    reader = SSAConfigReader("dummy")

    ssa = reader.get_secstructartist()

    assert ssa is mock_ssa_instance
    mock_ssa_class.assert_called_once()


def test_get_secstructartist_cached(monkeypatch, minimal_config):
    monkeypatch.setattr(
        "secstructartist.config.configreader.load_configuration",
        lambda *_: minimal_config
    )

    monkeypatch.setattr(
        "secstructartist.config.configreader.PRIMITIVES_AVAIL",
        {"circle": lambda **kwargs: MagicMock()}
    )

    monkeypatch.setattr(
        "secstructartist.config.configreader.ElementArtist",
        lambda **kwargs: MagicMock()
    )

    monkeypatch.setattr(
        "secstructartist.config.configreader.SecStructArtist",
        MagicMock()
    )

    reader = SSAConfigReader("dummy")

    s1 = reader.get_secstructartist()
    s2 = reader.get_secstructartist()

    assert s1 is s2