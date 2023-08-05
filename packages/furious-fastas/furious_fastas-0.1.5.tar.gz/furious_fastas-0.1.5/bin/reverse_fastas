#!/usr/bin/env python3
import argparse
from pathlib import Path

from furious_fastas import fastas, contaminants, Fastas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reverse a uniprot fasta file and translate it to general ncbi format.')
    parser.add_argument("fasta_file", help="Path to the fasta file.")
    parser.add_argument("-conts",
                        "--contaminants",
                        action='store_const',
                        const=True,
                        default=False,
                        help="Append Tenzer's contaminants.")
    a = parser.parse_args()
    fasta_file = Path(a.fasta_file).expanduser()
    fastas = fastas(fasta_file)
    if a.contaminants:
    	fastas.extend(contaminants)
    	out_name = fasta_file.stem+'_reversed_contaminated'+fasta_file.suffix
    else:
    	out_name = fasta_file.stem+'_reversed'+fasta_file.suffix
    fastas_general = Fastas(f.to_ncbi_general() for f in fastas)
    fastas_general.reverse()
    fastas_general.write(fasta_file.parent/out_name)
    print('Success!')
