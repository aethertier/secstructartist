import pytest
from unittest.mock import MagicMock
from secstructartist.config import SSAConfigWriter


# ---------------------------------------------------------------------
# Minimal Stub Classes
# ---------------------------------------------------------------------

class DummyPrimitive:
    def __init__(self, type_, **kwargs):
        self._dict = {"type": type_, **kwargs}

    def to_dict(self):
        return dict(self._dict)

class DummyElement:
    def __init__(self, label, primitives):
        self.label = label
        self.primitives = primitives

class DummyDrawstyle:
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return dict(self._data)

class DummySecStructArtist:
    def __init__(self, elements, drawstyle):
        self.elements = elements
        self.drawstyle = drawstyle


# ---------------------------------------------------------------------
# Primitive Registration
# ---------------------------------------------------------------------

def test_register_primitive_generates_key():
    writer = SSAConfigWriter()
    prim = DummyPrimitive("circle", radius=5)
    key = writer.register_primitiveartist(prim)
    assert key.startswith("circle-")
    assert key in writer._primitives
    assert writer._primitives[key]["radius"] == 5


def test_register_primitive_same_object_returns_same_key():
    writer = SSAConfigWriter()
    prim = DummyPrimitive("rect", width=2)
    key1 = writer.register_primitiveartist(prim)
    key2 = writer.register_primitiveartist(prim)
    assert key1 == key2
    assert len(writer._primitives) == 1


def test_register_primitive_different_objects_same_content_get_unique_keys():
    writer = SSAConfigWriter()
    prim1 = DummyPrimitive("circle", radius=3)
    prim2 = DummyPrimitive("circle", radius=3)
    key1 = writer.register_primitiveartist(prim1)
    key2 = writer.register_primitiveartist(prim2)
    # Different objects → different keys (even if content same)
    assert key1 != key2
    assert len(writer._primitives) == 2


# ---------------------------------------------------------------------
# Element Registration
# ---------------------------------------------------------------------

def test_register_elementartist():
    writer = SSAConfigWriter()
    prim = DummyPrimitive("circle", radius=2)
    element = DummyElement("helix", [prim])
    key = writer.register_elementartist(element, element_key="H")
    assert key == "H"
    assert "H" in writer._elements
    assert writer._elements["H"]["label"] == "helix"
    assert len(writer._elements["H"]["primitives"]) == 1


def test_register_element_duplicate_key_raises():
    writer = SSAConfigWriter()
    prim = DummyPrimitive("circle", radius=2)
    element = DummyElement("helix", [prim])
    writer.register_elementartist(element, "H")
    with pytest.raises(ValueError):
        writer.register_elementartist(element, "H")


# ---------------------------------------------------------------------
# SecStructArtist Registration
# ---------------------------------------------------------------------

def test_register_secstructartist():
    prim = DummyPrimitive("circle", radius=2)
    element = DummyElement("helix", [prim])
    elements = {"H": element}
    drawstyle = DummyDrawstyle({"linewidth": 2})
    artist = DummySecStructArtist(elements, drawstyle)
    writer = SSAConfigWriter()
    writer.register_secstructartist(artist)
    data = writer.get_dict()
    assert "H" in data["elements"]
    assert data["drawstyle"]["linewidth"] == 2
    assert len(data["primitives"]) == 1


# ---------------------------------------------------------------------
# Reset
# ---------------------------------------------------------------------

def test_reset_clears_registry():
    writer = SSAConfigWriter()
    prim = DummyPrimitive("circle", radius=1)
    writer.register_primitiveartist(prim)
    writer.reset()
    assert writer._drawstyle == {}
    assert writer._elements == {}
    assert writer._primitives == {}
    assert writer._primitives_ids == {}


# ---------------------------------------------------------------------
# get_dict
# ---------------------------------------------------------------------

def test_get_dict_structure():
    writer = SSAConfigWriter()
    d = writer.get_dict()
    assert set(d.keys()) == {"drawstyle", "elements", "primitives"}


# ---------------------------------------------------------------------
# write() delegation
# ---------------------------------------------------------------------

def test_write_delegates(monkeypatch):
    writer = SSAConfigWriter()
    spy = MagicMock(return_value="written")
    monkeypatch.setattr(
        "secstructartist.config.configwriter.write_configuration",
        spy
    )
    result = writer.write("file.json", format_="json")
    spy.assert_called_once()
    assert result == "written"