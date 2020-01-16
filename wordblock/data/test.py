from unittest import TestCase
from random import randint, choice
from string import ascii_lowercase

from .base import DatabaseBase
from .words import Word
from .prefences import Prefences
from .wordUseage import WordUseage

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

class Test_Prefences(TestCase):

        def setUp(self):
            self.fileLoc = './ds.test.json'
            return super().setUp()

        def test_set(self):

            obj = Prefences(self.fileLoc).set('testPref', str(randint(0, 5000)))

            self.assertIsInstance(
                obj,
                bool
            )

            self.assertTrue(
                obj
            )

        def test_get(self):

            obj = Prefences(self.fileLoc).get('testPref')
            self.assertIsInstance(obj, dict)

class Test_WordUseage(TestCase):

    def setUp(self):
        self.fileLoc = './ds.test.json'
        return super().setUp()

    def test_insert(self):
    
        obj = WordUseage(self.fileLoc)

        for i in range(50):
            rowid = obj.insert(
                randint(0, 10000)
            )

            self.assertIsInstance(
                rowid,
                int
            )

    def test_getCounts(self):
        obj = WordUseage(self.fileLoc).getCounts()

        self.assertIsInstance(
            obj,
            dict
        )

        for k in obj.keys():
            self.assertIsInstance(
                k,
                int
            )

