%load_ext autoreload
%autoreload 2

from pathlib import Path

from furious_fastas.fasta import Fasta, fasta
from furious_fastas.fastas import Fastas
from collections import Counter
from furious_fastas.contaminants import contaminants


path = Path("/home/matteo/Projects/pep2prot/pep2prot/data/")
list(path.glob('*'))

mouse = Fastas()
mouse.read(path/'mouse.fasta')

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
