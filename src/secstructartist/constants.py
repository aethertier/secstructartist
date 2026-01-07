from pathlib import Path

SSA_VERSION = '2.0.0'

SSA_ROOT = Path(__file__).parent
SSA_DEFAULT_CONFIG = SSA_ROOT / 'config' / 'default.yaml'
SSA_DSSP_CONFIG = SSA_ROOT / 'config' / 'dssp.yaml'