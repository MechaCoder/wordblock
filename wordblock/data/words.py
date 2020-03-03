from .base import DatabaseBase, TinyDB, Query, time_ns, ascii_letters, DatabaseObject
from bs4 import BeautifulSoup
from urllib.request import urlopen
from fuzzywuzzy import process
from .wordsWeighting import WordWeighting


def getWordsFromUrl(url: str, wordSize: int = 5):

    httpObj = urlopen(url)
    html = httpObj.read().decode('utf8')
    httpObj.close()

    wordList = []
    for tag in BeautifulSoup(html, 'html.parser').select('p'):

        for word in tag.text.split():
            if len(word) < wordSize:
                continue

            if word in wordList:
                continue

            if vaildWords(word) is False:
                continue

            if word not in wordList:
                wordList.append(word)

    return wordList


def vaildWords(word: str):
    word = word.lower()
    if isinstance(word, str) is False:
        return False

    if word[0] not in ascii_letters:
        return False

    if word[-1] not in ascii_letters:
        return False

    for char in word:
        if char not in ascii_letters:
            return False

    return True


class Word(DatabaseBase):

    def __init__(self, filelocation='./ds.json', table=__name__):
        """ this is the database table for the table in this case
        `wordblock.data.words` """
        super().__init__(filelocation=filelocation, table=table)
        self.normalise()

        if len(self.all()) == 0:
            for word in getWordsFromUrl(
                    'https://en.wikipedia.org/wiki/Dyslexia'):
                try:
                    self.insert(word)
                except BaseException:
                    pass

    def incrementWordWegight(self, word):
        """ will attempt to find a word and add 1 to the weighting"""

        try:
            wordW = WordWeighting()
            wordRow = self.getRowByWord(wordW)
            wordW.increment(wordRow['id'])
            return True
        except BaseException:
            return False



    def insert(self, word: str,):
        """ insert a new word to the table """

        word = word.lower()

        tdb = DatabaseObject(self.file, self.table)
        tbl = tdb.tbl

        if tbl.contains(Query().word == word.lower()):
            self.incrementWordWegight(word.lower())


        rowId = tbl.insert({
            'word': word.lower(),
            'time': time_ns()
        })

        tdb.tdb.close()
        return rowId

    def insert_muiple(self, wordsList:list):

        tdb = DatabaseObject(self.file, self.table)
        tbl = tdb.tbl
        wordW = WordWeighting()

        convertedList = []
        for word in wordsList:
            word = word.lower()
            
            if isinstance(word, str) == False:
                continue

            if tbl.contains(Query().word == word.lower()):
                self.incrementWordWegight(word.lower())

            d = {
                'word': word.lower(),
                'time': time_ns()
            }
            convertedList.append(d)
        rowids = tbl.insert_multiple(convertedList)

        tdb.tdb.close()
        return rowids
        

    def readAllAsList(self):
        """ returns a list of all words with in the system """

        rows = []
        for word in self.all():
            rows.append(word['word'].lower())

        rows.sort()

        return rows

    def readFindString(self, qStr: str = '', rows: bool = False):
        if qStr == '':
            return self.readAllAsList()[0:72]

        words = self.readAllAsList()
        rWords = []
        for result in process.extract(qStr, words, limit=70):
            rWords.append(result[0])
        return rWords

    def normalise(self):

        idsList = []
        doneWords = []
        for word in self.all():

            if vaildWords(word['word'].lower()) is False:
                idsList.append(word['id'])

            if word['word'].lower() in doneWords:
                idsList.append(word['id'])

            doneWords.append(word['word'].lower())

        return self.removeById(idsList)

    def getRowByWord(self, word: str):
        tdb = DatabaseObject(self.file, self.table)
        tbl = tdb.tbl

        row = tbl.get(Query().word == word)

        tdb.tdb.close()
        return self.__outputRow__(row)
