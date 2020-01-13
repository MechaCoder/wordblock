from unittest import TestCase
from random import randint, choice
from string import ascii_lowercase

from .base import DatabaseBase
from .words import Word

def _makeRandomString(self, strLength:int = 10):

    returnStr = ''
    for x in range(strLength):
        chariter = choice(ascii_lowercase)
        returnStr += chariter

    return returnStr

class Test_DatabaseBase(TestCase):

    def setUp(self):
        self.fileLoc = './ds.test.json'
        return super().setUp()

    def test_all(self):

        rows = DatabaseBase(self.fileLoc).all()

        self.assertIsInstance(
            rows,
            list
        )

        for row in rows:

            self.assertIsInstance(row, dict)

    def test_removeById(self):

        self.assertTrue(
            DatabaseBase(self.fileLoc).removeById([])
        )

class Test_Word(TestCase):

    def setUp(self):
        self.fileLoc = './ds.test.json'
        return super().setUp()

    def test_insert(self):

        obj = Word(self.fileLoc)

        for i in range(50):
            rowid = obj.insert(
                _makeRandomString(10)
            )

            self.assertIsInstance(
                rowid,
                int
            )
