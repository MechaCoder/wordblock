from .words import Word  # noqa: F401
from .prefences import Prefences  # noqa: F401
from .wordUseage import WordUseage  # noqa: F401
from .wordsWeighting import WordWeighting #noqa: F401

from wordblock.ai import AIbase


def getCountPannel(findStr: str):

    wordObj = Word()
    weighting = WordWeighting()

    wordCounts = WordUseage().getCounts()
    allWords = wordObj.readFindString(findStr)
    sortedWords = []
    wordsCount = []
    wordsCountWithoutCount = []

    aiUid = Prefences().get('ai-id')['val']

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
        if Prefences().get('ai'):
            if wordRow['id'] is aiUid:
                counts.insert(0, wordRow)
                continue

        if int(wordRow['count']) is 0:
            nonCounts.append(wordRow)
            continue
        counts.append(wordRow)
        
    counts_reverse = sorted(counts, key=lambda i: i['count'])
    counts_reverse.reverse()
    nonCounts = sorted(nonCounts, key=lambda i: i['word'])
    return counts_reverse + nonCounts




