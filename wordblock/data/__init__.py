from .words import Word  # noqa: F401
from .prefences import Prefences  # noqa: F401
from .wordUseage import WordUseage  # noqa: F401
from .wordsWeighting import WordWeighting #noqa: F401


def getCountPannel(findStr: str):

    wordObj = Word()
    weighting = WordWeighting()

    wordCounts = WordUseage().getCounts()
    allWords = wordObj.readFindString(findStr)
    sortedWords = []
    wordsCount = []
    wordsCountWithoutCount = []

    allwordsrows = []
    for word in allWords:
        row = wordObj.getRowByWord(word)
        row['count'] = 0
        if row['id'] in wordCounts.keys():
            row['count'] = wordCounts[row['id']]

        if weighting.wightingExists(row['id']):
            row['count'] = row['count'] + int(weighting.get(row['id'])['value_id'])
        allwordsrows.append(row)

    counts = []
    nonCounts = []
    for wordRow in allwordsrows:
        if int(wordRow['count']) is 0:
            nonCounts.append(wordRow)
            continue
        counts.append(wordRow)
        
    counts_reverse = sorted(counts, key=lambda i: i['count'])
    counts_reverse.reverse()
    nonCounts = sorted(nonCounts, key=lambda i: i['word'])
    return counts_reverse + nonCounts




