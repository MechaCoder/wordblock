from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from .data import Word
from .utils import importer, isURLValid
from .speaker import speak
from .addWords import AddWordsApp
from clipPad import Clipper


class ToolBar(GridLayout):

    def __init__(self, **kwargs):
        """ this is where the Tools for the bar for importing"""
        super().__init__(**kwargs)
        self.rows = 1
        self.height = 10
        
        self.btn = Button(text='Add Words', on_press=self.on_press_callback)
        self.add_widget(self.btn)

    def on_press_callback(self, ints):
        print('text')
        pass


class WordScreen(GridLayout):

    def __init__(self, findTxt: str = '', **kwargs):
        """ this is the contoler for the word block """
        super().__init__(**kwargs)

        self.serchTerm = findTxt
        self.cols = 10
        self.block = {}

        for word in Word().readFindString(self.serchTerm):
            self.block[word] = Button(text=word, on_press=self.onPress)
            self.add_widget(self.block[word])

    def onPress(self, instance):
        Clipper().copy(instance.text)
        speak(instance.text)


class WordBlock(App):
    """ this is the app controller that is the root of the gui """

    def build(self):

        self.box = BoxLayout(orientation='vertical', spacing=5)
        self.tools = ToolBar(size_hint_y=0.15)
        self.sBox = TextInput(
            text="",
            size_hint_y=0.15,
            multiline=False,
            on_text_validate=self.findWords
        )
        self.word = WordScreen(self.sBox.text)

        self.refreshWidgets("")
        return self.box

    def findWords(self, value):
        self.refreshWidgets('')

    def refreshWidgets(self, instance):

        self.word = WordScreen(self.sBox.text)

        self.box.clear_widgets()
        self.box.add_widget(self.tools)
        self.box.add_widget(self.sBox)
        self.box.add_widget(self.word)
        self.box.add_widget(
            Button(
                text='Refresh Window',
                on_press=self.refreshWidgets,
                size_hint_y=0.075
            )
        )
