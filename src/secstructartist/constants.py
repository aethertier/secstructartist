from pathlib import Path

SSA_VERSION = '2.0.0'

SSA_ROOT = Path(__file__).parent

SSA_CONFIGURATIONS = {
    'default': SSA_ROOT / 'config' / 'default.yaml',
    'dssp': SSA_ROOT / 'config' / 'dssp.yaml'
}