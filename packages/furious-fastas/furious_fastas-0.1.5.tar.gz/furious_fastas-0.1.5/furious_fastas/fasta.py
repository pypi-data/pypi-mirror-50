class Fasta(object):
    """Class representing one particular fasta object."""
    def __init__(self, header, sequence):
        self.sequence = sequence
        self.header = header

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.header)

    def __str__(self):
        return self.sequence

    def reverse(self):
        return self.__class__(self.header+" REVERSED", self.sequence[::-1])

    def copy(self):
        return self.__class__(self.header, self.sequence)

    def __hash__(self):
        return hash((self.sequence, self.header))


class ParsedFasta(Fasta):
    def __init__(self, accession, entry, description, sequence):
        self.accession = accession
        self.entry = entry
        self.description = description
        self.sequence = sequence

    def to_swissprot(self):
        return SwissProtFasta(self.accession, self.entry, self.description, self.sequence)

    def to_trembl(self):
        return TRemblFasta(self.accession, self.entry, self.description, self.sequence)

    def to_ncbi_general(self):
        return NCBIgeneralFasta(self.accession, self.entry, self.description, self.sequence)

    def __repr__(self):
        return "{}({}|{}|{})".format(self.__class__.__name__, self.accession, self.entry, self.description)

    @property
    def header(self):
        raise NotImplementedError("Header must be a valid fiel/accessor of any subclass of the ParsedFasta.")


class SwissProtFasta(ParsedFasta):
    def reverse(self, i=''):
        return Fasta('>REVERSE{} Reversed Sequence {}'.format(str(i), str(i)), self.sequence[::-1])

    @property
    def header(self):
        return ">sp|{}|{} {}".format(self.accession, self.entry, self.description)


class TRemblFasta(ParsedFasta):
    def reverse(self, i=''):
        return Fasta('>REVERSE{} Reversed Sequence {}'.format(str(i), str(i)), self.sequence[::-1])

    @property
    def header(self):
        return ">tr|{}|{} {}".format(self.accession, self.entry, self.description)


class NCBIgeneralFasta(ParsedFasta):
    def reverse(self, i=''):
        return Fasta('>gnl|db|REVERSE{} REVERSE{} Reversed Sequence {}'.format(str(i), str(i), str(i)), self.sequence[::-1])        
    @property
    def header(self):
        return ">gnl|db|{} {} {}".format(self.accession, self.entry, self.description)


def parse_header(h):
    if ">gnl|db|" in h:
        h = h.replace(">gnl|db|","")
        accession, entry = h.split(' ')[:2]
        description = h.replace(accession +' '+ entry + ' ', '')
        db = ">gnl|db|"
    elif '>sp|' in h:
        h = h.replace('>sp|','')
        accession, h = h.split('|')
        entry = h.split(' ')[0]
        description = h.replace(entry+' ','')
        db = ">sp|"
    elif '>tr|' in h:
        h = h.replace('>tr|','')
        accession, h = h.split('|')
        entry = h.split(' ')[0]
        description = h.replace(entry+' ','')
        db = ">tr|"
    elif ">REVERSE" in h:
        h = h.replace('>','')
        accession = entry = h.split(' ')[0]
        description = h.replace(entry+' ','')
        db = ">sp|"
    else:
        raise RuntimeError("Header cannot be parsed: {}".format(h))
    return accession, entry, description, db


fasta_formats = {'>sp|':      SwissProtFasta,
                 '>tr|':      TRemblFasta,
                 '>gnl|db|':  NCBIgeneralFasta}

def fasta(header, sequence):
    try:
        accession, entry, description, db = parse_header(header)
        fasta_format = fasta_formats.get(db, Fasta)
        return fasta_format(accession, entry, description, sequence)
    except RuntimeError:
        return Fasta(header, sequence)
