from .words import Word  # noqa: F401
from .prefences import Prefences # noqa: F401
from .wordUseage import WordUseage # noqa: F401

def getCountPannel(findStr:str):

    wordObj = Word()

    wordCounts = WordUseage().getCounts()
    allWords = wordObj.readFindString(findStr)
    sortedWords = []

    for word in allWords:
        row = wordObj.getRowByWord(word)
        row['count'] = 0
        if row['id'] in wordCounts.keys():
            row['count'] = wordCounts[ row['id'] ]
        
        sortedWords.append(row)
    sortedWords = sorted(sortedWords, key=lambda i: i['count'])
    sortedWords.reverse()
    return sortedWords
