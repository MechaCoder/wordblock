from wordblock.prefences import Prefences
from .base import AIbase


def processAiData():
    obj = AIbase()
    obj.processData()
    obj.train()
    return True

def setPrediction():
    obj = AIbase()
    prodictedid = obj.predict()
    Prefences().set('ai-id', prodictedid)
    return True