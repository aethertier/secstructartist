import pytest
from pathlib import Path

from secstructartist.constants import SSA_CONFIGURATION_PRESETS
from secstructartist.config import SSAConfigReader


@pytest.mark.parametrize("name,path", SSA_CONFIGURATION_PRESETS.items())
def test_default_configuration_files_exist(name, path):
    """
    All declared configuration paths must exist on disk.
    """
    assert isinstance(path, Path)
    assert path.exists(), f"Configuration '{name}' does not exist at {path}"


@pytest.mark.parametrize("name,path", SSA_CONFIGURATION_PRESETS.items())
def test_default_configurations_load(name, path):
    """
    All default configurations must load successfully
    and produce a SecStructArtist.
    """
    reader = SSAConfigReader(path)
    artist = reader.get_secstructartist()

    assert artist is not None