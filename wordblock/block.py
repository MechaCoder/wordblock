from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from .data import Word
from .utils import importer, isURLValid
from .speaker import speak
from clipPad import Clipper

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

Builder.load_string("""
<WordBlock>
    name: '_word_block_'
""")


class ToolBar(GridLayout):

    def __init__(self, **kwargs):
        """ this is where the Tools for the bar for importing"""
        super().__init__(**kwargs)
        self.rows = 1
        self.height = 10
        self.urlText = TextInput(hint_text="enter a url")
        self.importPage = Button(text='Import URL', on_press=self.onClick)

        self.add_widget(self.urlText)
        self.add_widget(self.importPage)

    def onClick(self, instance):
        if isURLValid(self.urlText.text) is False:
            return False

        self.urlText.disabled = True
        self.importPage.disabled = True

        importer(self.urlText.text)

        self.urlText.disabled = False
        self.importPage.disabled = False
        p = Popup(
            title="A new Webpage has been imported",
            size_hint=(None, None),
            size=(200, 200),
        )
        p.content = Button(text='Dismiss', on_press=p.dismiss)
        p.open()
        self.urlText.text = ""


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

        self.add_widget(self.box)

    def findWords(self, event):
        pass



sm = ScreenManager()
sm.add_widget(WordBlock())

class WordBlock(App):
    """ this is the app controller that is the root of the gui """

    def build(self):
        sm.current = '_word_block_'
        return sm
