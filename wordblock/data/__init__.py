from .words import Word  # noqa: F401
from .prefences import Prefences # noqa: F401
from .wordUseage import WordUseage # noqa: F401

def getCountPannel(findStr:str):

    wordCounts = WordUseage().getCounts()
    allWords = Word().readFindString(findStr)


    for wordRow in allWords:
        wordRow['count'] = 0
        if wordRow['id'] in wordCounts.keys():
            wordRow['count'] = wordCounts[ wordRow['id'] ]

    sortedWords = sorted(
        allWords,
        key=lambda i: i['count']
    )
    sortedWords.reverse()
    return sortedWords
    