import pytest
from pathlib import Path

from secstructartist.constants import SSA_PRESETS
from secstructartist.config import SSAConfigReader


@pytest.mark.parametrize("name,path", SSA_PRESETS.items())
def test_default_configuration_files_exist(name, path):
    """
    All declared configuration paths must exist on disk.
    """
    assert isinstance(path, Path)
    assert path.exists(), f"Configuration '{name}' does not exist at {path}"


@pytest.mark.parametrize("name,path", SSA_PRESETS.items())
def test_default_configurations_load(name, path):
    """
    All default configurations must load successfully
    and produce a SecStructArtist.
    """
    reader = SSAConfigReader(path)
    artist = reader.get_secstructartist()

    assert artist is not None

@pytest.mark.parametrize("alias", SSA_PRESETS._SSA_PRESET_ALIASES.keys())
def test_aliases(alias):
    """
    Test that all aliases return an existing path.
    """
    path = SSA_PRESETS[alias]
    assert isinstance(path, Path)
    assert path.exists(), f"Configuration '{alias}' does not exist at {path}"
