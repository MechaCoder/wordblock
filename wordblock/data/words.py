from .base import *

class Word(DatabaseBase):

    def __init__(self, filelocation='./ds.json', table=__name__):
        super().__init__(filelocation=filelocation, table=table)

    def insert(self, word:str):
        
        tdb = TinyDB(self.file)
        tbl = tdb.table(self.table)

        if tbl.contains(Query().word == word):
            raise Warning(f'{word} already exists')

        rowId = tbl.insert({
            'word': word,
            'time': time_ns()
        })

        tdb.close()
        return rowId

    def readAllAsList(self):
        """ returns a list of all words with in the system """

        rows = []
        for word in self.all():
            rows.append(word['word'])

        return rows
