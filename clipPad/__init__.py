import pyperclip


class ClipperException(Exception):
    pass


class Clipper:

    def __init__(self):
        """ this where a string can be added to the clipbard """
        super().__init__()

    def copy(self, msg: str):
        """ writes a string to the clipboard """

        if isinstance(msg, str) is False:
            raise ClipperException('the message must be a string')

        try:
            pyperclip.copy(msg)
        except pyperclip.PyperclipException:
            raise ClipperException(
                "There has been been issue with pyperclip. \n make sure you have xsel or xclip installed" # noqa E501
            )
