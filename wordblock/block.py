from time import sleep
from threading import Thread

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from .data import Word
from .utils import importer, isURLValid
from clipPad import Clipper




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
        if isURLValid(self.urlText.text) == False:
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
        p.content=Button(text='Dismiss', on_press=p.dismiss)
        p.open()
        self.urlText.text = ""

        
        

class WordScreen(GridLayout):

    def __init__(self, **kwargs):
        """ this is the contoler for the word block """
        super().__init__(**kwargs)
        self.cols = 10
        self.block = {}

        for word in Word().readAllAsList():
            self.block[word] = Button(text=word, on_press=self.onPress)
            self.add_widget(self.block[word])

            # continue

            if len(self.block.keys()) >= 60:
                break

    def onPress(self, instance):
        Clipper().copy(instance.text)

class WordBlock(App):
    """ this is the app controller that is the root of the gui """
     
    def build(self):
 

        self.box = BoxLayout(orientation='vertical', spacing=10)
        
        self.tools = ToolBar(size_hint_y=0.125)
        self.word = WordScreen()

        self.refreshWidgets("")
        return self.box

    def refreshWidgets(self, instance):

        self.word = WordScreen()

        self.box.clear_widgets()
        self.box.add_widget(self.tools)
        self.box.add_widget(self.word)
        self.box.add_widget(
            Button(text='Refresh Window', on_press=self.refreshWidgets, size_hint_y=0.075)
        )


        print('refresh')