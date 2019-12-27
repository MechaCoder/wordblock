from time import sleep
from threading import Thread

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from .data import Word
from .utils import importer, isURLValid
from clipPad import Clipper




class ToolBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.height = 10
        self.urlText = TextInput(hint_text="enter a url")
        self.importPage = Button(text='Import URL', on_press=self.onClick)
        self.add_widget(self.urlText)
        self.add_widget(self.importPage)

    def onClick(self, instance):
        

        if isURLValid(self.urlText.text) == False:
            return False

        self.urlText.disabled = True
        self.importPage.disabled = True
        importer(self.urlText.text)
        self.urlText.disabled = False
        self.importPage.disabled = False

        print('Finished')

class WordScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.block = {}

        for word in Word().readAllAsList():
            self.block[word] = Button(text=word, on_press=self.onPress)
            self.add_widget(self.block[word])

    def onPress(self, instance):
        Clipper().copy(instance.text)



class WordBlock(App):
     
    def build(self):
 
        self.box = BoxLayout(orientation='vertical', spacing=20)
        self.tools = ToolBar(size_hint_y=0.075)
        self.word = WordScreen()

        self.box.add_widget(self.tools)
        self.box.add_widget(self.word)

        return self.box
