from .words import Word  # noqa: F401
from .prefences import Prefences  # noqa: F401
from .wordUseage import WordUseage  # noqa: F401
from .wordsWeighting import WordWeighting #noqa: F401
from .base import DatabaseException

from wordblock.ai.base import AIbase


def getCountPannel(findStr: str):

    wordObj = Word()
    weighting = WordWeighting()

    wordCounts = WordUseage().getCounts()
    allWords = wordObj.readFindString(findStr)
    sortedWords = []
    wordsCount = []
    wordsCountWithoutCount = []

    try:
        aiUid = Prefences().get('ai-id')['val']
    except DatabaseException:
        aiUid = 0

    allwordsrows = []
    for word in allWords:

        row = wordObj.getRowByWord(word) # gets the word row

        row['count'] = 0
        
        if row['id'] in wordCounts.keys(): # sets the useage
            row['count'] = wordCounts[row['id']] 

        if weighting.wightingExists(row['id']): #  sets the weighting
            row['count'] = row['count'] + int(weighting.get(row['id'])['value_id'])
        
        allwordsrows.append(row)

    counts = []
    nonCounts = []
    aiValue = None
    
    for wordRow in allwordsrows:
        if Prefences().get('ai'):
            if wordRow['id'] == aiUid:
                aiValue = wordRow
                continue


        if int(wordRow['count']) is 0:
            nonCounts.append(wordRow)
            continue
        counts.append(wordRow)
        
    counts_reverse = sorted(counts, key=lambda i: i['count'])
    counts_reverse.reverse()
    
    nonCounts = sorted(nonCounts, key=lambda i: i['word'])
    returnlist = counts_reverse + nonCounts
    
    if isinstance(aiValue, dict):
        returnlist.insert(0, aiValue)
    
    return returnlist




