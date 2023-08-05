import subprocess as proc

import pandas as pd

from reciprocalblast.db import BlastDB
from reciprocalblast.match import BlastSeq


class BlastnSearch(object):
    blastn_cmd = (
        'blastn -query {query} -out {out} -db {db} '
        '-task {task} -outfmt {outfmt} '
        '-max_target_seqs {max_target_seqs} -max_hsps {max_hsps} '
        '-num_threads {num_threads}')
    
    def __init__(
        self, query_path:str, out_path:str, db:BlastDB,
        task:str='blastn', outfmt:str='"6 std qlen slen qcovs sstrand"',
        max_target_seqs:int=1, max_hsps:int=1, 
        eval_threshold:float=1e-10, num_threads:int=1, run:bool=True,
    ):
        """Performs a blastn search of query sequences against a blast database.

        Parameters
        ----------
        query_path : str
            Path of the query sequences file.
        out_path : str
            Path to save the blastn results table.
        db : BlastDB
            BlastDB object that represents the blast database to be used.
        task : str, optional
            blastn search algorithm to used, by default 'blastn'
        outfmt : str, optional
            Output format configuration, 
            by default '"6 std qlen slen qcovs sstrand"'
        max_target_seqs : int, optional
            Maximum number of aligned sequences to keep, by default 1
        max_hsps : int, optional
            Maximum number of high-scoring pair (HSP) to keep for each query-subject alignment, by default 1
        eval_threshold : float, optional
            Maximum expect value for retaining hits, by default 1e-10
        num_threads : int, optional
            Number of threads to use in the blast search, by default 1
        run : bool, optional
            If True, runs the blast search and overwrites existing results.
            Otherwise, assumes that blast search has been performed previously
            and will only import the results, by default True
        """
        self.query_path = query_path
        self.out_path = out_path
        self.db = db.db_path if isinstance(db, BlastDB) else db
        self.task = task
        self.outfmt = outfmt
        self.max_target_seqs = max_target_seqs
        self.max_hsps = max_hsps
        self.result = None
        
        if run:
            self.run(num_threads=num_threads)
        self.result = self.parse_result(out_path, eval_threshold)

    def run(self, num_threads:int=1):
        """Runs blast search.

        Parameters
        ----------
        num_threads : int, optional
            Number of threads to use in the blast search, by default 1

        Raises
        ------
        SystemError
            Raised when blastn returns a non-zero return code.
        """
        blastn_cmd = type(self).blastn_cmd.format(
            query=self.query_path,
            out=self.out_path,
            db=self.db,
            task=self.task,
            outfmt=self.outfmt,
            max_target_seqs=self.max_target_seqs,
            max_hsps=self.max_hsps,
            num_threads=num_threads)
        res = proc.run(blastn_cmd, shell=True)
        if res.returncode != 0:
            raise SystemError(f'blastn failed: {blastn_cmd}')

    @staticmethod
    def parse_result(path:str, eval_threshold:float=1e-10) -> pd.DataFrame:
        """Reads the blast result csv into a pandas DataFrame.
        
        Parameters
        ----------
        path : str
            Path of blastn results file.
        eval_threshold : float, optional
            Maximum expect value for retaining hits, by default 1e-10
        
        Returns
        -------
        pandas.DataFrame
            Returns the blastn results after removing hits above the
            specified expect value threshold.
        """
        col_labels = ['qaccver', 'saccver', 'pident', 'length', 
                      'mismatch', 'gapopen', 'qstart', 'qend', 
                      'sstart', 'send', 'evalue', 'bitscore', 
                      'qlen', 'slen', 'qcovs', 'sstrand']
        ref_df = pd.read_csv(path, sep='\t', header=None, index_col=None)
        ref_df.columns = col_labels
        filtered_df = ref_df[ref_df['evalue'] < eval_threshold]
        return filtered_df.set_index(['qaccver', 'saccver'])
    
    def __repr__(self):
        return f'BlastnSearch(query={self.query_path}, db={self.db}, task={self.task})'


class ReciprocalBlastnSearch(object):
    def __init__(
        self, seq1_fasta:str, seq2_fasta:str, seq1_db:BlastDB, seq2_db:BlastDB,
        seq1_out:str='', seq2_out:str='',
        task:str='blastn', outfmt:str='"6 std qlen slen qcovs sstrand"',
        max_target_seqs:int=1, max_hsps:int=1, 
        eval_threshold:int=1e-10, num_threads:int=1,
        run:bool=True,
    ):
        """Performs reciprocal blastn search between two sets of sequences.
        
        Parameters
        ----------
        seq1_fasta : str
            Path to file with the first set of sequences.
        seq2_fasta : str
            Path to file with the second set of sequences.
        seq1_db : BlastDB
            Path to blast db created from the first set of sequences.
        seq2_db : BlastDB
            Path to blast db created from the second set of sequences.
        seq1_out : str, optional
            Path where to save the forward (seq1 v. seq2) blastn search,
            by default ''
        seq2_out : str, optional
            Path where to save the reverse (seq2 v. seq1) blastn search,
            by default ''
        task : str, optional
            blastn search algorithm to used, by default 'blastn'
        outfmt : str, optional
            Output format configuration, 
            by default '"6 std qlen slen qcovs sstrand"'
        max_target_seqs : int, optional
            Maximum number of aligned sequences to keep, by default 1
        max_hsps : int, optional
            Maximum number of high-scoring pair (HSP) to keep for each query-subject alignment, by default 1
        eval_threshold : float, optional
            Maximum expect value for retaining hits, by default 1e-10
        num_threads : int, optional
            Number of threads to use in the blast search, by default 1
        run : bool, optional
            If True, runs the blast search and overwrites existing results.
            Otherwise, assumes that blast search has been performed previously
            and will only import the results, by default True
        """
        self.seq1_fasta = seq1_fasta
        self.seq2_fasta = seq2_fasta
        self.seq1_db = (
            seq1_db.db_path if isinstance(seq1_db, BlastDB) else seq1_db)
        self.seq2_db = (
            seq2_db.db_path if isinstance(seq2_db, BlastDB) else seq2_db)
        self.seq1_out = seq1_out if seq1_out else seq1_fasta + '.blastn.txt'
        self.seq2_out = seq2_out if seq2_out else seq2_fasta + '.blastn.txt'
        self.task = task
        self.outfmt = outfmt
        self.max_target_seqs = max_target_seqs
        self.max_hsps = max_hsps
        self.result1 = None
        self.result2 = None
        self._reciprocal_matches = None
        
        if run:
            self.run(num_threads=num_threads)

        self.result1 = BlastnSearch.parse_result(self.seq1_out, eval_threshold)
        self.result2 = BlastnSearch.parse_result(self.seq2_out, eval_threshold)

    def run(self, num_threads=1):
        """Runs reciprocal blast search.
        
        Parameters
        ----------
        num_threads : int, optional
            Number of threads to use in the blast search, by default 1
        
        Raises
        ------
        SystemError
            Raised when either forward or reverse blastn search
            returns a non-zero return code.
        """
        res1 = proc.run(
            BlastnSearch.blastn_cmd.format(
                query=self.seq1_fasta,
                out=self.seq1_out,
                db=self.seq2_db,
                task=self.task,
                outfmt=self.outfmt,
                max_target_seqs=self.max_target_seqs,
                max_hsps=self.max_hsps,
                num_threads=num_threads,
            ),
            shell=True,
        )
        if res1.returncode != 0:
            raise SystemError('Forward blastn search failed to run.')
        res2 = proc.run(
            BlastnSearch.blastn_cmd.format(
                query=self.seq2_fasta,
                out=self.seq2_out,
                db=self.seq1_db,
                task=self.task,
                outfmt=self.outfmt,
                max_target_seqs=self.max_target_seqs,
                max_hsps=self.max_hsps,
                num_threads=num_threads,
            ),
            shell=True,
        )
        if res2.returncode != 0:
            raise SystemError('Reverse blastn search failed to run.')
            
    @staticmethod
    def parse_result(out1:str, out2:str, eval_threshold=1e-10) -> pd.DataFrame:
        """Reads the blast result csv into a pandas DataFrame.
        
        Parameters
        ----------
        out1 : str
            Path of forward blastn results file.
        out2 : str
            Path of reverse blastn results file.
        eval_threshold : float, optional
            Maximum expect value for retaining hits, by default 1e-10
        
        Returns
        -------
        pandas.DataFrame
            Returns the blastn results after removing hits above the
            specified expect value threshold.
        """
        result1 = BlastnSearch.parse_result(out1, eval_threshold)
        result2 = BlastnSearch.parse_result(out2, eval_threshold)
        # Create relationship graphs
        blastseq_d = {}
        # Process result 1
        for k, v in result1.iterrows():
            # process keys
            query_id, ref_id = k            
            # query id
            if query_id not in blastseq_d.keys():
                query_blastseq = BlastSeq(query_id)
                blastseq_d[query_id] = query_blastseq
            else:
                query_blastseq = blastseq_d[query_id]
            # ref id
            if ref_id not in blastseq_d.keys():
                ref_blastseq = BlastSeq(ref_id)
                blastseq_d[ref_id] = ref_blastseq
            else:
                ref_blastseq = blastseq_d[ref_id]
            ref_blastseq.add_query_match(query_blastseq, v)
        # Process result 2
        for k, v in result2.iterrows():
            # process keys
            query_id, ref_id = k
            # query id
            if query_id not in blastseq_d.keys():
                query_blastseq = BlastSeq(query_id)
                blastseq_d[query_id] = query_blastseq
            else:
                query_blastseq = blastseq_d[query_id]
            # ref id
            if ref_id not in blastseq_d.keys():
                ref_blastseq = BlastSeq(ref_id)
                blastseq_d[ref_id] = ref_blastseq
            else:
                ref_blastseq = blastseq_d[ref_id]
            ref_blastseq.add_query_match(query_blastseq, v)
        # Get reciprocal matches
        reciprocal_matches = []
        for seq in blastseq_d.values():
            reciprocal_matches += seq.reciprocal_matches()
        return list(set(sorted(
            reciprocal_matches, 
            key=lambda s: s.seq1.name + s.seq2.name
        )))

    def reciprocal_matches(self, eval_threshold:float=1e-10) -> list:
        """Returns the list of reciprocal blast matches computed from
        the forward and reverse blastn searches.
        
        Parameters
        ----------
        eval_threshold : float, optional
            Maximum expect value for retaining hits, by default 1e-10
        
        Returns
        -------
        list
            List of ReciprocalBlastMatch objects representing
            reciprocal matches between two sequences.
        """
        if not self._reciprocal_matches:
            self._reciprocal_matches =\
                self.parse_result(self.seq1_out, self.seq2_out, eval_threshold)
        return self._reciprocal_matches

    def reciprocal_matched_df(self, eval_threshold:float=1e-10) -> pd.DataFrame:
        """Returns the list of reciprocal blast matches as a pandas DataFrame.
        
        Parameters
        ----------
        eval_threshold : float, optional
            Maximum expect value for retaining hits, by default 1e-10
        
        Returns
        -------
        list
            DataFrame containing the reciprocal matches between two sequences.
        """
        index = pd.MultiIndex.from_tuples(
            [(m.seq1.name, m.seq2.name) for m in self.reciprocal_matches()],
            names=['seq1', 'seq2'])
        return pd.DataFrame.from_records(
            [m.metadata for m in reciprocal_matches], 
            index=index)

    def __repr__(self):
        return (
            f'ReciprocalBlastnSearch(seq1_fasta={self.seq1_fasta}, '
            f'seq2_fasta={self.seq2_fasta}, task={self.task})')
