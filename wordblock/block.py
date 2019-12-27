from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from .data import Word
from clipPad import Clipper

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
 
        self.box = BoxLayout(orientation='horizontal', spacing=20)
        self.word = WordScreen()
        self.box.add_widget(self.word)

        return self.box
