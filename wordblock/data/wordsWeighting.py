from .base import DatabaseBase, DatabaseException, TinyDB, Query, time_ns


class WordWeighting(DatabaseBase):

    def __init__(self, filelocation='./ds.json', table=__name__):
        super().__init__(filelocation=filelocation, table=table)

    def set(self, wordId: int, valueId: int):

        tdb = DatabaseObject(self.file, self.table)
        tbl = tdb.tbl

        rows = tbl.upsert({
            'word_id': wordId,
            'value_id': valueId
        }, Query().word_id == wordId)
        tdb.tdb.close()
        return rows

    def get(self, tag: str):
        tdb = DatabaseObject(self.file, self.table)
        tbl = tdb.tbl

        row = tbl.get(Query().word_id == tag)
        tdb.tdb.close()

        return self.__outputRow__(row)

    def wightingExists(self, tag: str):
    
        tdb = DatabaseObject(self.file, self.table)
        tbl = tdb.tbl

        existing = tbl.contains(Query().word_id == tag)
        tdb.tdb.close()

        return existing
