from tinydb import TinyDB, Query
from tinydb.database import Document
from time import time_ns

class DatabaseException(Exception): pass

class DatabaseBase:

    def __init__(self, filelocation:str='./ds.json', table:str=__name__):
        self.file = filelocation
        self.table = table

    def __outputRow__(self, doc:Document):
        """ returns a dict of the id and all the keys within the document """

        if isinstance(doc, Document) == False:
            raise DatabaseException('the object passed must be a `tinydb.database.Document`.')

        rDict = {'id': doc.doc_id}
        for key in doc.keys():
            rDict[key] = doc[key]

        return rDict

    def __outputRows__(self, docs:list):
        
        if isinstance(docs, list) == False:
            raise DatabaseException('the object passed must be a `list`.')
        rows = []
        for doc in docs:
            rows.append(self.__outputRow__(doc))

        return rows

    def all(self):

        tdb = TinyDB(self.file)
        tbl = tdb.table(self.table)

        rows = tbl.all()
        tdb.close()

        return self.__outputRows__(rows)

    def getById(self, docId:int):

        if isinstance(docId, int) == False:
            raise DatabaseException('docIds must be a int')

        tdb = TinyDB(self.file)
        tbl = tdb.table(self.table)

        row = tbl.get(doc_id=docId)
        tdb.close()

        return row

