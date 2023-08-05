import pandas as pd


class BlastSeq(object):
    def __init__(self, name:str, metadata:dict=None):
        """Creates a new sequence representation.

        Parameters
        ----------
        name : str
            Unique name of the sequence
        metadata : dict, optional
            Relavant data about the sequence, by default None
        """
        self._name = name
        self.metadata = metadata
        self._query_matches = {}
    
    @property
    def name(self):
        return self._name

    @property
    def query_matches(self):
        return self._query_matches    
    
    @property
    def num_query_matches(self):
        return len(self._query_matches)
    
    def reciprocal_matches(self) -> list:
        """Returns the list of reciprocal blastn matches involving
        this sequence.

        Returns
        -------
        list
            List of ReciprocalBlastMatch objects representing
            reciprocal matches between this sequence and zero
            or more other sequences.
        """
        matches = []
        # look into query matches 
        for query, meta in self._query_matches.items():
            for r, rmeta in query._query_matches.items():
                if r == self:
                    matches.append(
                        ReciprocalBlastMatch(self, query, meta, rmeta))
        return matches
    
    def add_query_match(self, query, metadata=None):
        """Adds a blast match between this sequence as reference and
        the other sequence as query.

        Parameters
        ----------
        query : BlastSeq
            BlastSeq object representating the query sequence.
        metadata : dict-like, optional
            Relevant data about the match. 
            Usually a row in the blast results table, by default None
        """
        self._query_matches[query] = BlastMatch(query, self, metadata)
        
    def __repr__(self):
        return f'BlastSeq({self.name})'

    def __eq__(self, other):
        return (
            (self.name == other.name) and 
            len(self.query_matches) == len(other.query_matches)
        )
    
    def __hash__(self):
        return hash(self.name)


class BlastMatch(object):
    def __init__(self, query:BlastSeq, ref:BlastSeq, metadata=None):
        """Create a representation of a blast match between two sequences.

        Parameters
        ----------
        query : BlastSeq
            Query sequence
        ref : BlastSeq
            Reference/subject (database) sequence
        metadata : dict-like, optional
            Relevant metadata about the match.
            Usually a row in the blast results table, by default None
        """
        self.query = query
        self.ref = ref
        # metadata
        self.length = None
        self.mismatch = None
        self.gapopen = None
        self.qstart = None
        self.qend = None
        self.sstart = None
        self.send = None
        self.evalue = None
        self.bitscore = None
        self.qlen = None
        self.slen = None
        self.qcovs = None
        self.sstrand = None
        
        self._parse_metadata_(metadata)

    @property
    def metadata(self):
        return pd.Series({
            'pident': self.pident,
            'length': self.length,
            'mismatch': self.mismatch,
            'gapopen': self.gapopen,
            'qstart': self.qstart,
            'qend': self.qend,
            'sstart': self.sstart,
            'send': self.send,
            'evalue': self.evalue,
            'bitscore': self.bitscore,
            'qlen': self.qlen,
            'slen': self.slen,
            'qcovs': self.qcovs,
            'sstrand': self.sstrand,
        })

    def _parse_metadata_(self, metadata):
        if metadata is not None:
            self.pident = (
                metadata['pident'] if 'pident' in metadata.keys() else None)
            self.length = (
                metadata['length'] if 'length' in metadata.keys() else None)
            self.mismatch = (
                metadata['mismatch'] if 'mismatch' in metadata.keys() else None)
            self.gapopen = (
                metadata['gapopen'] if 'gapopen' in metadata.keys() else None)
            self.qstart = (
                metadata['qstart'] if 'qstart' in metadata.keys() else None)
            self.qend = metadata['qend'] if 'qend' in metadata.keys() else None
            self.sstart = (
                metadata['sstart'] if 'sstart' in metadata.keys() else None)
            self.send = metadata['send'] if 'send' in metadata.keys() else None
            self.evalue = (
                metadata['evalue'] if 'evalue' in metadata.keys() else None)
            self.bitscore = (
                metadata['bitscore'] if 'bitscore' in metadata.keys() else None)
            self.qlen = metadata['qlen'] if 'qlen' in metadata.keys() else None
            self.slen = metadata['slen'] if 'slen' in metadata.keys() else None
            self.qcovs = (
                metadata['qcovs'] if 'qcovs' in metadata.keys() else None)
            self.sstrand = (
                metadata['sstrand'] if 'sstrand' in metadata.keys() else None)
    
    def __repr__(self):
        return f'BlastMatch(query={self.query.name}, ref={self.ref.name})'

    def __eq__(self, other):
        return (
            (self.query == other.query) and
            (self.ref == other.ref) and
            (self.length == other.length) and
            (self.mismatch == other.mismatch) and
            (self.gapopen == other.gapopen) and
            (self.qstart == other.qstart) and
            (self.qend == other.qend) and
            (self.sstart == other.sstart) and
            (self.send == other.send) and
            (self.evalue == other.evalue) and
            (self.bitscore == other.bitscore) and
            (self.qlen == other.qlen) and
            (self.slen == other.slen)
        )


class ReciprocalBlastMatch(object):
    tuple_index = pd.MultiIndex.from_tuples([
        (match, prop) 
        for match in ['forward', 'reverse']
        for prop in [
            'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend',
            'sstart', 'send', 'evalue', 'bitscore', 'qlen', 'slen', 'qcovs',
            'sstrand']
        ], names=['match', 'property'])

    def __init__(
        self, seq1:BlastSeq, seq2:BlastSeq, forward_match:BlastMatch, reverse_match:BlastMatch
    ):
        """Create a representation of a reciprocal blast match between
        two sequences.

        Parameters
        ----------
        seq1 : BlastSeq
            Query sequence
        seq2 : BlastSeq
            Reference/subject (database) sequence
        forward_match : BlastMatch
            Match object for the forward (seq1 v. seq2) blast search.
        reverse_match : BlastMatch
            Match object for the reverse (seq21 v. seq1) blast search.
        """
        self.seq1 = seq1
        self.seq2 = seq2
        # metadata
        self.match1 = forward_match
        self.match2 = reverse_match
    
    @property
    def metadata(self):
        values = (
            list(self.match1.metadata.values) + 
            list(self.match2.metadata.values))
        return pd.Series(values, index=type(self).tuple_index)

    def __repr__(self):
        return (
            f'ReciprocalBlastMatch(seq1={self.seq1.name}, '
            f'seq2={self.seq2.name})'
        )

    def __eq__(self, other):
        return (
            (
                (self.seq1 == other.seq1) or
                (self.seq1 == other.seq2)
            ) and
            (
                (self.seq2 == other.seq2) or
                (self.seq2 == other.seq1)
            ) and
            ((
                (self.match1 == other.match1) and
                (self.match2 == other.match2)
            ) or 
            (
                (self.match1 == other.match2) and
                (self.match2 == other.match1)
            ))
        )

    def __hash__(self):
        return hash(tuple(sorted([self.seq1, self.seq2], key=lambda s: s.name)))
