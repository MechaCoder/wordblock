from .base import DatabaseBase, DatabaseException
from string import ascii_letters  # noqa: F401
from time import time_ns  # noqa: F401

from tinydb import TinyDB
from tinydb import Query  # noqa: F401
from tinydb.database import Document


class Prefences(DatabaseBase):

    def __init__(self, filelocation='./ds.json', table=__name__):
        super().__init__(filelocation=filelocation, table=table)

        if self.settingExists('speak') is False:
            self.set('speak', True)

        if self.settingExists('makeCaps') is False:
            self.set('makeCaps', False)

    def set(self, tag: str, value):

        tdb = TinyDB(self.file)
        tbl = tdb.table(self.table)

        rows = tbl.upsert({
            'tag': tag,
            'val': value
        }, Query().tag == tag)

        tdb.close()

        return True

    def get(self, tag: str):
        tdb = TinyDB(self.file)
        tbl = tdb.table(self.table)

        row = tbl.get(Query().tag == tag)
        tdb.close()

        return self.__outputRow__(row)

    def settingExists(self, tag: str):

        tdb = TinyDB(self.file)
        tbl = tdb.table(self.table)

        existing = tbl.contains(Query().tag == tag)
        tdb.close()

        return existing
