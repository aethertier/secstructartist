from dataclasses import dataclass
from typing import Generator, Tuple
import pandas as pd

def stripped_str(s: str) -> str:
    return str(s).strip()

def ie_tuple(s: str) -> Tuple[int, float]:
    idx, energy = s.split(',')
    return int(idx), float(energy)

DSSP_COLUMNS = [
    # Column Name, Start, Stop, Type
    ("dssp_index", 0, 5, int),
    ("residue_number", 5, 10, int),
    ("chain", 11, 12, str),
    ("aa", 13, 14, stripped_str),
    ("structure", 16, 25, str),
    ("bp1", 26, 29, int),
    ("bp2", 30, 33, int),
    ("acc", 34, 38, int),
    ("nh_o1", 40, 50, ie_tuple),
    ("o_nh1", 51, 61, ie_tuple),
    ("nh_o2", 62, 72, ie_tuple),
    ("o_nh2", 73, 83, ie_tuple),
    ("tco", 86, 91,float),
    ("kappa", 91, 97, float),
    ("alpha", 97, 103, float),
    ("phi", 103, 109, float),
    ("psi", 109, 115, float),
    ("x_ca", 116, 122, float),
    ("y_ca", 123, 129, float),
    ("z_ca", 130, 136, float),
]


@dataclass(frozen=True)
class DSSPData:
    header: dict
    sequence: str
    structure: str
    residues: pd.DataFrame


def iterate_lines(file_path, **kwargs) -> Generator[str, None, None]:
    with open(file_path, **kwargs) as fh:
        for line in fh:
            yield line


def read_dssp(file_path: str) -> DSSPData:

    lines = iterate_lines(file_path, mode='r')

    # -------------------------
    # 1. Parse header
    # -------------------------
    header = {}

    for line in lines:
        if line.startswith("HEADER"):
            header["header"] = line.strip()
        elif line.startswith("COMPND"):
            header["compound"] = line.strip()
        elif line.startswith("SOURCE"):
            header["source"] = line.strip()
        elif "TOTAL NUMBER OF RESIDUES" in line:
            header["n_residues"] = int(line.split()[0])
        elif "ACCESSIBLE SURFACE" in line:
            header["accessible_surface"] = float(line.split()[0])
        elif line.startswith("  #  RESIDUE"):
            break
    else:
        raise ValueError("Could not find DSSP table start")

    # -------------------------
    # 2. Parse table
    # -------------------------
    records = []

    for line in lines:
        if not line.strip():
            continue

        # Fixed-width parsing (based on DSSP format)
        record = {
            n: t(line[i:j]) for n,i,j,t in DSSP_COLUMNS
        }


        records.append(record)

    df = pd.DataFrame(records)
    sequence = ''.join(df['aa'])
    structure = ''.join(df['structure'].str[0])

    # Optional consistency checks
    if len(sequence) != len(structure):
        print("Warning: sequence length != structure length")
    if len(sequence) != len(df):
        print("Warning: sequence length != residue table length")

    return DSSPData(
        header = header,
        sequence = sequence,
        structure = structure,
        residues = df,
    )