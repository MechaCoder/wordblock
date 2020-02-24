from kivy.config import Config
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock

from wordblock.data import Word, Prefences, WordUseage, getCountPannel
from wordblock.speaker import speak
from wordblock.settings import WordsListLayout, UrlLayout, AddSingle, SearchLayoutEdit
from wordblock.prefences import PrefencesGui
from wordblock.share import ShareBox
from wordblock.ai import AIbase
from clipPad import Clipper


Builder.load_string("""
<WordBlockScreen>
    name: '_word_block_'
<SettingsScreen>
    name: '_settings_'
<PrefencesScreen>
    name: '_prefences_'
<SplahScreen>
    name: '_splash_'
""")


class PannelToolBar(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.btn_wordblock = Button(
            text='word block',
            on_press=self.change_screen
        )
        self.btn_setting = Button(
            text='settings',
            on_press=self.change_screen
        )
        self.btn_prefences = Button(
            text='prefences',
            on_press=self.change_screen
        )

        self.cols = 3

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


class WordGrid(GridLayout):

    def __init__(self, findTxt: str = '', **kwargs):
        """ this is the contoler for the word block """
        super().__init__(**kwargs)

        self.serchTerm = findTxt
        self.cols = 8
        self.block = {}

        for wordRow in getCountPannel(self.serchTerm):
            word = wordRow['word']

            if Prefences().get('makeCaps')['val']:
                word = word.upper()

            self.block[word.lower()] = Button(text=word, on_press=self.onPress)
            self.block[word.lower()].padding = (0.5, 1)
            self.add_widget(self.block[word.lower()])

    def onPress(self, instance):
        wordRow = Word().getRowByWord(instance.text.lower())
        WordUseage().insert(wordRow['id'])
        Clipper().copy(instance.text.lower())
        if Prefences().get('speak')['val']:
            speak(instance.text)


class WordBlockScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #  import Form
        self.box = BoxLayout(
            orientation='vertical',
            spacing=5
        )

        self.importBox = PannelToolBar()
        self.importBox.size_hint_y = None
        self.importBox.height = 30
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

        self.box = BoxLayout(
            orientation='vertical',
            spacing=5
        )

        self.toolbar = PannelToolBar()
        self.toolbar.size_hint_y = None
        self.toolbar.height = 30
        self.box.add_widget(self.toolbar)

        self.addBtnSingle = AddSingle()
        self.box.add_widget(self.addBtnSingle)

        self.sBox = SearchLayoutEdit()
        self.box.add_widget(self.sBox)

        self.add_widget(self.box)

    def on_enter(self):
        super().on_enter()
        self.box.remove_widget(self.sBox)
        self.sBox = SearchLayoutEdit()
        self.box.add_widget(self.sBox)


class PrefencesScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        self.box = BoxLayout(orientation='vertical', spacing=5)
        self.pannelToolBar = PannelToolBar()
        self.pannelToolBar.size_hint_y = None
        self.pannelToolBar.height = 30
        
        self.box.add_widget(self.pannelToolBar)
        self.box.add_widget(PrefencesGui())

        self.add_widget(self.box)



class SplahScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        self.box = BoxLayout(orientation='vertical', spacing=5)
        self.box.add_widget(Image(source='assets/logo.png'))
        self.add_widget(self.box)

        self.clockEvent = Clock.schedule_once(self.changeToApp, 30)

    def changeToApp(self, b):
        sm.current = '_word_block_'
        Clock.unschedule(self.clockEvent)


sm = ScreenManager()
sm.add_widget(SplahScreen())
sm.add_widget(WordBlockScreen())
sm.add_widget(SettingsScreen())
sm.add_widget(PrefencesScreen())


class MainApp(App):

    def build(self):
        self.title = "WordBlock"
        sm.current = '_splash_'
        return sm


if __name__ == '__main__':

    ai = AIbase()
    # trainingFile = ai.processData() # this seams to crash the app whould a subprocess be better
    predictedId = ai.predict() ## sets a prodiction value to settings
    Prefences().set('ai-id', predictedId)

    fuctWidth = Window.size[0] + (Window.size[0] / 2)
    Window.size = (fuctWidth, 300)
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    MainApp().run()
