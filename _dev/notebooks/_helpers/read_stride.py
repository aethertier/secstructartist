from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class StrideData:
    header: dict
    sequence: str
    structure: str
    residues: pd.DataFrame


def iterate_lines(file_path, **kwargs):
    with open(file_path, **kwargs) as fh:
        for line in fh:
            yield line

def read_stride(file_path: str) -> StrideData:
    header = {}
    residues = []
    sequence_chunks = []
    structure_chunks = []

    for line in iterate_lines(file_path):
        line = line.rstrip("\n")

        # -------------------------
        # HEADER
        # -------------------------
        if line.startswith("HDR"):
            header["header"] = line.strip()
        elif line.startswith("CMP"):
            header.setdefault("compound", []).append(line.strip())
        elif line.startswith("SRC"):
            header.setdefault("source", []).append(line.strip())

        # -------------------------
        # SEQUENCE / STRUCTURE
        # -------------------------
        elif line.startswith("SEQ"):
            # SEQ  1    MLRPKALTQVLSQ...
            parts = line.split()
            seq = parts[2]
            sequence_chunks.append(seq)

        elif line.startswith("STR"):
            # STR          HHHHHHHH...
            seqlen = len(sequence_chunks[-1])
            structure_chunks.append(line[10:10+seqlen])

        # -------------------------
        # RESIDUE TABLE (ASG)
        # -------------------------
        elif line.startswith("ASG"):
            parts = line.split()

            # Example:
            # ASG  MET A    1    1    C          Coil    360.00    119.60     231.4

            record = {
                "resname": parts[1],
                "chain": parts[2],
                "resnum": int(parts[3]),
                "resid": int(parts[4]),  # often same as resnum
                "ss": parts[5],          # H, E, T, C
                "ss_full": parts[6],     # AlphaHelix, Strand, etc.
                "phi": float(parts[7]),
                "psi": float(parts[8]),
                "area": float(parts[9]),
            }

            residues.append(record)

    # -------------------------
    # Build outputs
    # -------------------------
    df = pd.DataFrame(residues)

    sequence = "".join(sequence_chunks)
    structure = "".join(structure_chunks)

    # Optional consistency checks
    if len(sequence) != len(structure):
        print("Warning: sequence length != structure length")
    if len(sequence) != len(df):
        print("Warning: sequence length != residue table length")

    return StrideData(
        header = header,
        sequence = sequence,
        structure = structure,
        residues = df,
    )