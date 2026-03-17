from collections.abc import Mapping
from pathlib import Path

__all__ = [
    'SSA_VERSION',
    'SSA_ROOT',
    'SSA_PRESETS'
]

SSA_VERSION = '2.2.0'
SSA_ROOT = Path(__file__).parent


class _SSAPresetRegistry(Mapping):

    _presets_prefix = SSA_ROOT / 'config' / 'presets'

    _SSA_PRESET_CONFIGFILES = {
        # HSL
        'hsl-outlined': _presets_prefix / 'hsl-outlined.yaml',
        'hsl-filled':   _presets_prefix / 'hsl-filled.yaml',
        'hsl-pymol':    _presets_prefix / 'hsl-pymol.yaml',
        'hsl-pymol2':   _presets_prefix / 'hsl-pymol2.yaml',
        'hsl-pymol3':   _presets_prefix / 'hsl-pymol3.yaml',

        # DSSP
        'dssp-dssp':    _presets_prefix / 'dssp-dssp.yaml',
        'dssp-stride':  _presets_prefix / 'dssp-stride.yaml',
    }

    _SSA_PRESET_ALIASES = {
        # HSL
        'default':      'hsl-pymol',
        'outlined':     'hsl-outlined',
        'filled':       'hsl-filled',
        'pymol':        'hsl-pymol',
        'pymol2':       'hsl-pymol2',
        'pymol3':       'hsl-pymol3',

        # DSSP
        'dssp':         'dssp-dssp',
        'stride':       'dssp-stride',
    }

    def __getitem__(self, key: str):
        preset = self._SSA_PRESET_ALIASES.get(key, key)
        preset_path = self._SSA_PRESET_CONFIGFILES.get(preset, None)
        if preset_path is None:
            raise KeyError(f"Unknown preset '{key}'")
        return preset_path
    
    def __iter__(self):
        return iter(self._SSA_PRESET_CONFIGFILES)

    def __contains__(self, key):
        preset = self._SSA_PRESET_ALIASES.get(key, key)
        return preset in self._SSA_PRESET_CONFIGFILES 

    def __len__(self):
        return len(self._SSA_PRESET_CONFIGFILES)


SSA_PRESETS = _SSAPresetRegistry()