from json import dumps
from time import time_ns

from mindsdb import Predictor

from wordblock.data import WordUseage, WordWeighting, Word


class AIbase:

    def __init__(self):
        super().__init__()
        self.modualName = 'wordblock-next-word-v2'
        self.fileName = 'aiData.3.json'

    def processData(self):
        """ this gets the data processes to a useable format and 
        writes to a file."""

        rows = []

        for each in WordUseage().all():
            rows.append(each)

        for each in WordWeighting().all():
            for x in range(0, each['value_id']):
                rows.append({
                    'wordId': each['word_id'],
                    'timeStamp': time_ns()
                })

        json = dumps(rows)
        filename = self.fileName
        with open(filename, 'w') as file:
            file.write(json)
            file.close()
        
        return filename


    def train(self):
        """ trains the AI modual """
        Predictor(self.modualName).learn(
            from_data=self.fileName,
            to_predict="id"
        )
        return True

    def predict(self):

        result = Predictor(name=self.modualName).predict()
        return round(result[0]['id'])