from .words import Word  # noqa: F401
from .prefences import Prefences  # noqa: F401
from .wordUseage import WordUseage  # noqa: F401


def getCountPannel(findStr: str):

    wordObj = Word()

    wordCounts = WordUseage().getCounts()
    allWords = wordObj.readFindString(findStr)
    sortedWords = []
    wordsCount = []
    wordsCountWithoutCount = []

    for word in allWords:
        row = wordObj.getRowByWord(word)
        row['count'] = 0
        if row['id'] in wordCounts.keys():
            row['count'] = wordCounts[row['id']]
            wordsCount.append(row)
            continue
        wordsCountWithoutCount.append(row)

    wordsCount = sorted(wordsCount, key=lambda i: i['count'])
    wordsCount.reverse()

    wordsCountWithoutCount = sorted(
        wordsCountWithoutCount,
        key=lambda i: i['word'])
    sortedWords = wordsCount + wordsCountWithoutCount
    return sortedWords
