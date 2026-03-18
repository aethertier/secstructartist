from dataclasses import dataclass
import pandas as pd

COLUMN_NAMES =  ['resid', 'resn', 'oneletter', 'ss']

@dataclass(frozen=True)
class PymolData:
    header: dict
    sequence: str
    structure: str
    residues: pd.DataFrame


def read_pymoltxt(file_path: str) -> PymolData:
    
    # Read file
    df = pd.read_csv(file_path, sep=' ', comment='#', names=COLUMN_NAMES)
    sequence = ''.join(df['oneletter'])
    structure = ''.join(df['ss'])

    # Optional consistency checks
    if len(sequence) != len(structure):
        print("Warning: sequence length != structure length")
    if len(sequence) != len(df):
        print("Warning: sequence length != residue table length")

    return PymolData(
        header = {},
        sequence = sequence,
        structure = structure,
        residues = df,
    )