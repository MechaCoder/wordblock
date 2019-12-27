from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


class WordScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4

        words = ['the', 'quick', 'brown', 'fox']
        self.block = {}

        for word in words:
            print
            self.block[word] = Button(text=word)
            self.add_widget(self.block[word])
        


class WordBlock(App):
     
    def build(self):
 
        self.box = BoxLayout(orientation='horizontal', spacing=20)
        self.word = WordScreen()
        self.box.add_widget(self.word)

        return self.box
 
    def clearText(self, instance):
 
        self.txt.text = ''
