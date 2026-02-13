from pathlib import Path

SSA_VERSION = '2.0.0'

SSA_ROOT = Path(__file__).parent

SSA_CONFIGURATIONS = {
    'simple': SSA_ROOT / 'config' / 'simple.yaml',
    'pymol': SSA_ROOT / 'config' / 'pymol.yaml',
    'dssp': SSA_ROOT / 'config' / 'dssp.yaml'
}