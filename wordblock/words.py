
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

from .data import Word, Prefences, WordUseage
from .speaker import speak
from .settings import WordsListLayout, UrlLayout, AddSingle
from .prefences import PrefencesGui
from clipPad import Clipper

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

Builder.load_string("""
<WordBlock>
    name: '_word_block_'
<SettingsScreen>
    name: '_settings_'
<PrefencesScreen>
    name: '_prefences_'
""")


class PannelToolBar(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.btn_wordblock = Button(
            text='word block',
            on_press=self.change_screen
        )
        self.btn_setting = Button(text='settings', on_press=self.change_screen)
        self.btn_prefences = Button(
            text='prefences',
            on_press=self.change_screen
        )

        # screenName = str(sm.current_screen)[14:-2]

        self.cols = 3
        self.size_hint_y = 0.25

        self.add_widget(self.btn_wordblock)
        self.add_widget(self.btn_setting)
        self.add_widget(self.btn_prefences)

    def change_screen(self, inst):
        if inst.text == self.btn_wordblock.text:
            sm.current = '_word_block_'
            return True

        if inst.text == self.btn_setting.text:
            sm.current = '_settings_'
            return True

        if inst.text == self.btn_prefences.text:
            sm.current = '_prefences_'
            return False


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

        # wordsList = Word().readFindString(self.serchTerm):
        for word in Word().readFindString(self.serchTerm):

            if Prefences().get('makeCaps')['val']:
                word = word.upper()

            self.block[word.lower()] = Button(text=word, on_press=self.onPress)
            self.add_widget(self.block[word.lower()])

    def onPress(self, instance):
        wordRow = Word().getRowByWord(instance.text)
        WordUseage().insert(wordRow['id'])
        Clipper().copy(instance.text)
        if Prefences().get('speak')['val']:
            speak(instance.text)


class WordBlock(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #  import Form
        self.box = BoxLayout(
            orientation='vertical',
            spacing=5
        )

        self.importBox = PannelToolBar()
        self.box.add_widget(self.importBox)

        self.searchBox = TextInput(
            text="",
            size_hint_y=0.15,
            multiline=False,
            on_text_validate=self.findWords
        )
        self.searchBox.bind(text=self.onTextChange)
        self.box.add_widget(self.searchBox)
        
        self.word = WordGrid(findTxt=self.searchBox.text)
        self.box.add_widget(self.word)
        
        self.findWords()
        self.add_widget(self.box)

    def findWords(self):
        self.box.remove_widget(self.word)
        self.word = WordGrid(findTxt=self.searchBox.text)
        self.box.add_widget(self.word)

    def onTextChange(self, instance, value):
        self.box.remove_widget(self.word)
        self.word = WordGrid(findTxt=self.searchBox.text)
        self.box.add_widget(self.word)

    def on_enter(self):
        super().on_enter()
        self.box.remove_widget(self.word)
        self.word = WordGrid(findTxt=self.searchBox.text)
        self.box.add_widget(self.word)


class SettingsScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.box = BoxLayout(orientation='vertical', spacing=5)

        self.urlPanel = UrlLayout(size_hint_y=1)
        self.addSingle = AddSingle(size_hint_y=1)

        self.wordList = WordsListLayout(spacing=10, size_hint_y=None)

        self.wordList.bind(minimum_height=self.wordList.setter('height'))

        self.scrollList = ScrollView(
            size_hint=(1, None),
            size=(Window.width, 175)
        )
        self.scrollList.add_widget(self.wordList)

        self.pannels = PannelToolBar()
        self.pannels.size_hint_y = 1.75

        self.box.add_widget(self.pannels)

        self.box.add_widget(self.urlPanel)
        self.box.add_widget(self.addSingle)
        self.box.add_widget(self.scrollList)

        self.add_widget(self.box)


class PrefencesScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        self.box = BoxLayout(orientation='vertical', spacing=5)
        self.box.add_widget(PannelToolBar())
        self.box.add_widget(PrefencesGui())

        self.add_widget(self.box)


sm = ScreenManager()
sm.add_widget(WordBlock())
sm.add_widget(SettingsScreen())
sm.add_widget(PrefencesScreen())


class WordBlock(App):
    """ this is the app controller that is the root of the gui """

    def build(self):
        sm.current = '_word_block_'
        return sm
