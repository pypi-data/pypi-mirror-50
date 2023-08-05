import subprocess as proc


class BlastDB(object):
    makeblastdb_cmd = (
        'makeblastdb -in {sequence_path} -input_type {input_type} '
        '-dbtype {dbtype} -title {title} -out {db_path}')
    
    def __init__(
        self, sequence_path:str, title:str, db_path:str,
        input_type:str='fasta', dbtype:str='nucl',
        run=True
    ):
        """Creates a new blast database.
        
        Parameters
        ----------
        sequence_path : str
            Path to sequences file.
        title : str
            Title of the database
        db_path : str
            Path where to save the database files
        input_type : str, optional
            Type of sequences input file, by default 'fasta'
        dbtype : str, optional
            Type of database to be constructed, by default 'nucl'
        
        Raises
        ------
        SystemError
            Raised when makeblastdb returns a non-zero return code.
        """
        self.title = title
        self.db_path = db_path
        self.dbtype = dbtype
        
        if run:
            self.run(sequence_path, input_type)

    def run(self, sequence_path, input_type):
        makeblastdb_cmd = type(self).makeblastdb_cmd.format(
            sequence_path=sequence_path,
            input_type=input_type,
            dbtype=self.dbtype,
            title=self.title,
            db_path=self.db_path)
        res = proc.run(makeblastdb_cmd, shell=True)
        if res.returncode != 0:
            raise SystemError(f'makeblastdb failed: {makeblastdb_cmd}')

    def __repr__(self):
        return f'BlastDB({self.title}, {self.db_path}, dbtype={self.dbtype})'
