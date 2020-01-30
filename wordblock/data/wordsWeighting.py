from .base import DatabaseBase, DatabaseException, TinyDB, Query, time_ns


class WordWeighting(DatabaseBase):

    def __init__(self, filelocation='./ds.json', table=__name__):
        super().__init__(filelocation=filelocation, table=table)

    def set(self, wordId: int, valueId: int):

        tdb = TinyDB(self.file)
        tbl = tdb.table(self.table)

        rows = tbl.upsert({
            'word_id': wordId,
            'value_id': valueId
        }, Query().word_id == wordId)
        tdb.close()
        return rows

    def get(self, tag: str):
        tdb = TinyDB(self.file)
        tbl = tdb.table(self.table)

        row = tbl.get(Query().tag == tag)
        tdb.close()

        return self.__outputRow__(row)
