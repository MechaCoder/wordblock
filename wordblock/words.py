from random import randint

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock

from .data import Word
from .utils import importer, isURLValid
from .speaker import speak
from .settings import *
from clipPad import Clipper

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

Builder.load_string("""
<WordBlock>
    name: '_word_block_'
<SettingsScreen>
    name: '_settings_'
""")

class ToolBar(GridLayout):

    def __init__(self, **kwargs):
        """ this is where the Tools for the bar for importing"""
        super().__init__(**kwargs)
        self.rows = 1
        self.height = 10
        
        self.btn = Button(text='Add Words', on_press=self.on_press_callback)
        self.add_widget(self.btn)

    def on_press_callback(self, ints):
        sm.current = '_settings_'
        pass

class WordGrid(GridLayout):

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

class WordBlock(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #  import Form
        self.box = BoxLayout(
            orientation='vertical',
            spacing=5
        )

        self.importBox = ToolBar(size_hint_y=0.15)
        self.box.add_widget(self.importBox)

        self.searchBox = TextInput(
            text="",
            size_hint_y=0.15,
            multiline=False,
            on_text_validate=self.findWords
        )
        self.box.add_widget(self.searchBox)

        self.word = WordGrid(findTxt=self.searchBox.text)
        self.box.add_widget(self.word)

        Clock.schedule_interval(self.findWords, 1)

        self.add_widget(self.box)

    def findWords(self, event):
        self.box.remove_widget(self.word)
        self.word = WordGrid(findTxt=self.searchBox.text)
        self.box.add_widget(self.word)
        pass

class SettingsScreen(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.box = BoxLayout(orientation='vertical', spacing=5)

        self.urlPanel = UrlLayout(size_hint_y=1)
        self.addSingle = AddSingle(size_hint_y=1)

        self.wordList = WordsListLayout(spacing=10, size_hint_y=None)
        self.wordList.bind(minimum_height=self.wordList.setter('height'))
        self.scrollList = ScrollView(size_hint=(1, None), size=(Window.width, 200))
        self.scrollList.add_widget(self.wordList)

        self.box.add_widget(Button(text='Word List', on_press=self.changePanel))
        self.box.add_widget(self.urlPanel)
        self.box.add_widget(self.addSingle)
        self.box.add_widget(self.scrollList)

        self.add_widget(self.box)

    def refreshList(self, inst):
        self.box.clear_widgets()

        self.urlPanel = UrlLayout(size_hint_y=1)
        self.addSingle = AddSingle(size_hint_y=1)
        
        self.wordList = WordsListLayout(spacing=10, size_hint_y=None)
        self.wordList.bind(
            minimum_height=self.wordList.setter('height')
        )
        
        self.scrollList = ScrollView(
            size_hint=(1, None),
            size=(Window.width, 200)
        )
        self.scrollList.add_widget(self.wordList)

        self.box.add_widget(self.urlPanel)
        self.box.add_widget(self.addSingle)
        self.box.add_widget(self.scrollList)

    def changePanel(self, inst):
        sm.current = '_word_block_'

sm = ScreenManager()
sm.add_widget(WordBlock())
sm.add_widget(SettingsScreen())

class WordBlock(App):
    """ this is the app controller that is the root of the gui """

    def build(self):
        sm.current = '_word_block_'
        return sm
