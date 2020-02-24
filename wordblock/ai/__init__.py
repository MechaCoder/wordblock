from wordblock.prefences import Prefences
from .base import AIbase


def processAiData():
    print('started processAIData')
    obj = AIbase()
    obj.processData()

    print('finished processAiData')
    return True

def setPrediction():
    obj = AIbase()
    prodictedid = obj.predict()
    Prefences().set('ai-id', prodictedid)