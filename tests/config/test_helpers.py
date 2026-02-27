import io
import json
import yaml
import pytest

from secstructartist.config._helpers import (
    infer_file_format,
    load_configuration,
    write_configuration,
)


# ---------------------------------------------------------------------
# infer_file_format
# ---------------------------------------------------------------------

def test_infer_file_format_auto_json():
    assert infer_file_format("file.json") == "json"


def test_infer_file_format_auto_yaml():
    assert infer_file_format("file.yaml") == "yaml"


def test_infer_file_format_explicit():
    assert infer_file_format("file.any", fmt="json") == "json"


def test_infer_file_format_invalid():
    with pytest.raises(ValueError):
        infer_file_format("file.txt")


# ---------------------------------------------------------------------
# load_configuration – path input
# ---------------------------------------------------------------------

def test_load_configuration_json_path(tmp_path):
    data = {"a": 1}
    p = tmp_path / "config.json"
    p.write_text(json.dumps(data))

    result = load_configuration(p)

    assert result == data


def test_load_configuration_yaml_path(tmp_path):
    data = {"a": 1}
    p = tmp_path / "config.yaml"
    p.write_text(yaml.safe_dump(data))

    result = load_configuration(p)

    assert result == data


# ---------------------------------------------------------------------
# load_configuration – file handle input
# ---------------------------------------------------------------------

def test_load_configuration_filehandle_json(tmp_path):
    data = {"a": 1}
    p = tmp_path / "config.json"
    p.write_text(json.dumps(data))

    with p.open("r") as fh:
        result = load_configuration(fh)

    assert result == data


def test_load_configuration_filehandle_auto_without_name_raises():
    fh = io.StringIO('{"a":1}')
    with pytest.raises(RuntimeError):
        load_configuration(fh)


# ---------------------------------------------------------------------
# load_configuration – named preset
# ---------------------------------------------------------------------

def test_load_configuration_named_preset(tmp_path, monkeypatch):
    data = {"a": 1}
    p = tmp_path / "preset.json"
    p.write_text(json.dumps(data))

    monkeypatch.setattr(
        "secstructartist.config._helpers.SSA_CONFIGURATION_PRESETS",
        {"preset": str(p)}
    )

    result = load_configuration("preset")

    assert result == data


def test_load_configuration_invalid_type():
    with pytest.raises(TypeError):
        load_configuration(123)


# ---------------------------------------------------------------------
# write_configuration – path output
# ---------------------------------------------------------------------

def test_write_configuration_json_path(tmp_path):
    data = {"a": 1}
    p = tmp_path / "out.json"

    write_configuration(data, p)

    assert json.loads(p.read_text()) == data


def test_write_configuration_yaml_path(tmp_path):
    data = {"a": 1}
    p = tmp_path / "out.yaml"

    write_configuration(data, p)

    assert yaml.safe_load(p.read_text()) == data


# ---------------------------------------------------------------------
# write_configuration – file handle output
# ---------------------------------------------------------------------

def test_write_configuration_filehandle_json(tmp_path):
    data = {"a": 1}
    p = tmp_path / "out.json"

    with p.open("w") as fh:
        write_configuration(data, fh)

    assert json.loads(p.read_text()) == data


def test_write_configuration_filehandle_auto_without_name_raises():
    fh = io.StringIO()
    with pytest.raises(RuntimeError):
        write_configuration({"a": 1}, fh)


def test_write_configuration_invalid_target():
    with pytest.raises(TypeError):
        write_configuration({"a": 1}, 123)