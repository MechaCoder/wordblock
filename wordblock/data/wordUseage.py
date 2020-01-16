from time import time_ns
from .base import DatabaseBase, TinyDB

class WordUseage(DatabaseBase):

    def __init__(self, filelocation='./ds.json', table=__name__):
        super().__init__(filelocation=filelocation, table=table)

    def insert(self, wordId: int):

        tdb = TinyDB(self.file)
        tbl = tdb.table(self.table)

        rid = tbl.insert({
            'wordId': wordId,
            'timeStamp': time_ns()
        })

        tdb.close()
        return rid

    def getCounts(self):

        returnObj = {}
        for row in self.all():
            if row['wordId'] not in returnObj.keys():
                returnObj[row['wordId']] = 0
            returnObj[row['wordId']] = returnObj[row['wordId']] + 1

        return returnObj
