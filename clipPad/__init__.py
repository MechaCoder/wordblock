import pyperclip

class ClipperException(Exception): pass

class Clipper:

    def __init__(self):
        super().__init__()

    def copy(self, msg:str):

        if isinstance(msg, str) == False:
            raise ClipperException('the message must be a string')

        try:
            pyperclip.copy(msg)
        except pyperclip.PyperclipException as err:
            raise ClipperException("There has been been issue with pyperclip. make sure you have xsel or xclip")

    