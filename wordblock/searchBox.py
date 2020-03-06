from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class SearchBox(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.searchBox = TextInput(
            text="",
            multiline=False,
            on_text_validate=self.makeSearch
        )

        self.btn = Button(
            text='Search',
            on_press=self.makeSearch
        )

        self.rows = 1

        self.add_widget(self.searchBox)
        self.add_widget(self.btn)

    def makeSearch(self, inst):
        try:
            if self.parent.parent.name == '_word_block_':
                self.parent.parent.findWords()
                return True
        except AttributeError:
            pass

        try:
            if self.parent.parent.parent.name == '_settings_':
                self.parent.changeShearchEvent('', '')
        except AttributeError:
            pass
        
