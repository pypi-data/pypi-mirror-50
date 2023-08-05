%load_ext autoreload
%autoreload 2

from pathlib import Path

from furious_fastas.fasta import Fasta, fasta
from furious_fastas import Fastas, fastas, contaminants
from collections import Counter

path = Path("/home/matteo/Projects/pep2prot/pep2prot/data/")
list(path.glob('*'))

mouse = fastas(path/'mouse.fasta')

mouse.fasta_types()
f = mouse[0]
frev = f.reverse(0)
frev.sequence
f.sequence

mouse.any_reversed()
mouse.reverse()
len(mouse.fasta_types())

len()

mouse.same_fasta_types()
Counter(Counter(f.entry for f in mouse).values())

human_path = Path('~/Projects/furious_fastas/data/human_raw.fasta').expanduser()
human = fastas(human_path)
human.fasta_types()
human_general = Fastas(f.to_ncbi_general() for f in human)
human_general.fasta_types()