from json import loads, dumps
from time import time_ns


def mkFileName():
    ts = str(time_ns())[-6:]
    return f"words-{ts}.words.json"


class FilesBase:

    def __init__(self, filePath: str):

        self.path = filePath

    def write(self, content: str):

        if isinstance(content, str) == False:
            raise TypeError(
                'the content of a file must be commited as a string')

        with open(self.path, 'w') as file:
            file.write(content)

        return True

    def read(self):

        with open(self.path, 'r') as file:
            fileContent = file.read()

        return fileContent


class JsonFiles(FilesBase):

    def __init__(self, filePath):
        super().__init__(filePath)

    def write(self, content: dict):

        if isinstance(content, dict) == False:
            raise TypeError('the content of a file must be a dict')

        contAsStr = dumps(content)
        super().write(contAsStr)

        return True

    def read(self):

        fileCont = super().read()
        return loads(fileCont)
