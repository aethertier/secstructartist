from pathlib import Path

SSA_VERSION = '2.1.4'

SSA_ROOT = Path(__file__).parent

SSA_CONFIGURATION_PRESETS = {
    #
    # -- Simple artists -- Support only HSL
    #
    'default': SSA_ROOT / 'config' / 'presets' / 'pymol1.yaml',
    'simple': SSA_ROOT / 'config' / 'presets' / 'simple.yaml',
    'pymol': SSA_ROOT / 'config' / 'presets' / 'pymol1.yaml',
    'pymol1': SSA_ROOT / 'config' / 'presets' / 'pymol1.yaml',
    'pymol2': SSA_ROOT / 'config' / 'presets' / 'pymol2.yaml',
    'pymol3': SSA_ROOT / 'config' / 'presets' / 'pymol3.yaml',

    #
    # -- Extended artists -- Full DSSP-support
    #
    'dssp': SSA_ROOT / 'config' / 'presets' / 'dssp.yaml',
    'stride': SSA_ROOT / 'config' / 'presets' / 'stride.yaml'
}