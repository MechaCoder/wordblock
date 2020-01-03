from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window


from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from .data import Word
from .utils import importer
from .utils import isURLValid
from .ui.popUp import popUp

class UrlLayout(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3
        
        self.urlText = TextInput(
            text=""
        )

        self.importBtn = Button(text='import page', on_press=self.on_click)

        self.add_widget(Label(text='Url page import'))
        self.add_widget(self.urlText)
        self.add_widget(self.importBtn)
    
    def on_click(self, inst):
        if isURLValid(self.urlText.text) is False:
            return False

        self.urlText.disabled == True
        self.importBtn.disabled == True
        
        importer(self.urlText.text)

        self.urlText.disabled == False
        self.importBtn.disabled == False


class AddSingle(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2

        # self.add_widget(Label(text='Add single'))
        self.txtBox = TextInput(text='', multiline=False)
        self.btn = Button(text='Input Word', on_press=self.onBtnClick)

        self.add_widget(self.txtBox)
        self.add_widget(self.btn)

    def onBtnClick(self, inst):

        if len(self.txtBox.text) == 0:
            return False

        self.txtBox.disabled = True
        self.btn.disabled = True

        try:
            Word().insert(self.txtBox.text)
            popUp('{} has been created.'.format(self.txtBox.text))
        except Warning as err:
            popUp(str(err))

        self.txtBox.disabled = False
        self.btn.disabled = False
        return True

class WordsListLayout(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2
        for word in Word().all():
            
            row = GridLayout()
            row.rows = 1
            row.height = 40
            row.size_hint_y = None
            row.add_widget(
                Label(text=f'{word["word"]}', size_hint_y=None, height=40 )
            )
            row.add_widget(
                Button(text=f'delete', size_hint_y=None, height=40 )
            )

            
            self.add_widget(row)
        

class AddWordsApp(App):

    def build(self):
        self.box = BoxLayout(orientation='vertical', spacing=5)
        
        self.urlPanel = UrlLayout(size_hint_y=10)
        self.addSingle = AddSingle(size_hint_y=10)
        
        self.wordList = WordsListLayout(spacing=10, size_hint_y=None)
        self.wordList.bind(minimum_height=self.wordList.setter('height'))
        self.scrollList = ScrollView(size_hint=(1, None), size=(Window.width, 500))
        self.scrollList.add_widget(self.wordList)
        

        self.box.add_widget(self.urlPanel)
        self.box.add_widget(self.addSingle)
        self.box.add_widget(self.scrollList)
        return self.box