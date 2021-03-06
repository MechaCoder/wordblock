from string import ascii_letters  # noqa: F401
from time import time_ns  # noqa: F401

from tinydb import TinyDB
from tinydb import Query  # noqa: F401
from tinydb.database import Document
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware


class DatabaseObject:

    def __init__(self, fileLocation: str, tableName: str = '_default'):
        super().__init__()
        self.tdb = TinyDB(fileLocation, storage=CachingMiddleware(JSONStorage))
        self.tbl = self.tdb.table(tableName, cache_size=30)

class DatabaseException(Exception):
    pass


class DatabaseBase:

    def __init__(self, filelocation: str = './ds.json', table: str = __name__):
        """ this is the base class for all Database interaction.
        the table is going to be set to the name string of the class,
        """
        self.file = filelocation
        self.table = table

    def __outputRow__(self, doc: Document):
        """ returns a dict of the id and all the keys within the document """

        if doc is None:
            raise DatabaseException(
                'No row has been found'
            )

        if isinstance(doc, Document) is False:
            raise DatabaseException(
                'the object passed must be a `tinydb.database.Document`.'
            )

        rDict = {'id': doc.doc_id}
        for key in doc.keys():
            rDict[key] = doc[key]

        return rDict

    def __outputRows__(self, docs: list):
        """ provides function to output list of documents """

        if isinstance(docs, list) is False:
            raise DatabaseException('the object passed must be a `list`.')
        rows = []
        for doc in docs:
            rows.append(self.__outputRow__(doc))

        return rows

    def all(self):
        """ provides a list of dicts of all document in the table"""

        tdb = DatabaseObject(self.file, self.table)

        rows = tdb.tbl.all()
        tdb.tdb.close()

        return self.__outputRows__(rows)

    def getById(self, docId: int):
        """ this gets a document by the doc id and returns of dict """

        if isinstance(docId, int) is False:
            raise DatabaseException('docIds must be a int')

        tdb = DatabaseObject(self.file, self.table)

        row = tdb.tbl.get(doc_id=docId)
        tdb.tdb.close()

        return self.__outputRow__(row)

    def removeById(self, docIds: list):

        for ident in docIds:
            if isinstance(ident, int) is False:
                raise DatabaseException('all ids must be a string')

        tdb = DatabaseObject(self.file, self.table)

        tdb.tbl.remove(
            doc_ids=docIds
        )

        tdb.tdb.close()
        return True
