from time import time_ns
from .files import JsonFiles, mkFileName
from wordblock.data import Word

class ShareFileMalformed(Exception):
    pass

class Share:

    def mkFile(self):
        filename = mkFileName()
        words = []
        for wordRow in Word().all():
            words.append(
                wordRow['word']
            )
        dictList = {"words": words, "unixTimeStamp": str(time_ns())}
        return JsonFiles(filename).write(dictList)

    def readWordsToDB(self, filePath):
        fileContent = JsonFiles(filePath).read()
        
        if 'words' not in fileContent.keys():
            raise ShareFileMalformed('no word list found in file')

        Word().insert_muiple(fileContent['words'])

        return True