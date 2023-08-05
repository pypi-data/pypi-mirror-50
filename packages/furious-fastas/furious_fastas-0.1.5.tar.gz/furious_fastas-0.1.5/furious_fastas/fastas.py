"""Classes representing collections of fastas."""
from collections import Counter

from .fasta import fasta


class FastasAlreadyReversedError(Exception):
    pass


class Fastas(list):
    def read(self, path, **parse_args):
        """Append fastas from a file."""
        with open(path, 'r') as f:
            raw = f.read()
        self.parse(raw, **parse_args) 

    def parse(self, raw):
        """Parse a raw string containing some fasta sequences.

        Args:
            raw (str): a raw string with fasta file contents.
            fasta (class): class to represent the fastas with. Either 'Fasta' or 'ParsedFasta'
        """
        all_lines = raw.splitlines()
        headers = []
        headers_idx = []
        for i, l in enumerate(all_lines):
            if l[0] == '>':
                headers.append(l)
                headers_idx.append(i)
        headers_idx.append(len(all_lines))
        headers_idx = iter(headers_idx)
        prev_idx = next(headers_idx) + 1
        for next_idx, header in zip(headers_idx, headers):
            sequence = "".join(all_lines[prev_idx:next_idx])
            self.append(fasta(header, sequence))
            prev_idx = next_idx + 1

    def write(self, path, mode='w+'):
        """Write file under the given path."""
        with open(path, mode) as h:
            for f in self:
                h.write("{}\n{}\n".format(f.header, f.sequence))

    def repeat_stats(self):
        """Get the distribution of shared fasta sequences."""
        return dict(Counter(Counter(f.sequence for f in self).values()))

    def any_reversed(self):
        return any("REVERSE" in f.header for f in self)

    def reverse(self):
        """Extend fastas by adding reversed sequences."""
        if not self.any_reversed():
            self.extend([f.reverse(i+1) for i,f in enumerate(self)])
        else:
            raise FastasAlreadyReversedError()

    def __add__(self, other):
        """Sum fastas."""
        out = self.__class__()
        out.extend(self)
        out.extend(other)
        return out

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, len(self))

    def fasta_types(self):
        return dict(Counter(f.__class__.__name__ for f in self))

    def same_fasta_types(self):
        return len(self.fasta_types()) == 1


def fastas(path):
    """Read in a fasta object from a given path.

    Args:
        path (str or pathlib.Path): Path to the fasta file.
    Returns:
        Fastas
    """
    fs = Fastas()
    fs.read(path)
    return fs