from .base import *
from fuzzywuzzy import process

def vaildWords(word:str):
    word = word.lower()
    
    if isinstance(word, str) == False:
        return False

    if word[0] not in ascii_letters:
        return False

    if word[-1] not in ascii_letters:
        return False

    for char in word:
        if char not in ascii_letters and char not in "-'":
            return False

    return True

class Word(DatabaseBase):

    def __init__(self, filelocation='./ds.json', table=__name__):
        """ this is the database table for the table in this case `wordblock.data.words` """
        super().__init__(filelocation=filelocation, table=table)
        self.normalise()

    def insert(self, word:str):
        """ insert a new word to the table """

        word = word.lower()
        
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
            rows.append(word['word'].lower())

        rows.sort()

        return rows

    def readFindString(self, qStr:str=''):
        if qStr == '':
            return self.readAllAsList()

        words = self.readAllAsList()
        rWords = []
        for result in process.extract(qStr, words, limit=65):
            rWords.append(result[0])
        return rWords

    def normalise(self):

        idsList = []
        doneWords = []
        for word in self.all():
            
            if vaildWords(word['word'].lower()) == False:
                idsList.append(word['id'])

            if word['word'] in doneWords:
                idsList.append(word['id'])
            
            doneWords.append(word['word'].lower())

            
        self.removeById(idsList)

