from pathlib import Path

SSA_VERSION = '2.0.0'

SSA_ROOT = Path(__file__).parent

SSA_CONFIGURATIONS = {
    #
    # -- Simple artists -- Support only HSL
    #
    'default': SSA_ROOT / 'config' / 'pymol1.yaml',
    'simple': SSA_ROOT / 'config' / 'simple.yaml',
    'pymol': SSA_ROOT / 'config' / 'pymol1.yaml',
    'pymol1': SSA_ROOT / 'config' / 'pymol1.yaml',
    'pymol2': SSA_ROOT / 'config' / 'pymol2.yaml',
    'pymol3': SSA_ROOT / 'config' / 'pymol3.yaml',

    #
    # -- Extended artists -- Full DSSP-support
    #
    'dssp': SSA_ROOT / 'config' / 'dssp.yaml',
    'stride': SSA_ROOT / 'config' / 'stride.yaml'
}