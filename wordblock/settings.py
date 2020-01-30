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
from .data import WordUseage
from .utils import importer
from .utils import isURLValid
from .ui.popUp import popUp


class UrlLayout(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3
        stuffHeight = 25

        self.urlText = TextInput(
            text="",
            size_hint_y=None,
            height=stuffHeight
        )

        self.importBtn = Button(
            text='import page',
            on_press=self.on_click, 
            size_hint_y=None,
            height=stuffHeight
        )

        # self.add_widget(Label(text='Url page import', height=stuffHeight))
        self.add_widget(self.urlText)
        self.add_widget(self.importBtn)

    def on_click(self, inst):
        if isURLValid(self.urlText.text) is False:
            return False

        self.urlText.disabled = True
        self.importBtn.disabled = True

        importer(self.urlText.text)

        self.urlText.disabled = False
        self.importBtn.disabled = False


class AddSingle(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2
        stuffHeight = 25

        # self.add_widget(Label(text='Add single'))
        self.txtBox = TextInput(text='', multiline=False, size_hint_y=None, height=stuffHeight)
        self.btn = Button(text='Input Word', on_press=self.onBtnClick, size_hint_y=None, height=stuffHeight)

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

        self.cols = 4
        self.buildList()

    def buildList(self, b=None):

        self.clear_widgets()

        obj = WordUseage().getCounts()

        wordsList = sorted(Word().all(), key=lambda i: i['word'])
        for word in wordsList:
            row = GridLayout()
            row.rows = 1
            row.height = 40
            row.size_hint_y = None

            

            row.add_widget(
                Label(text=f'{word["word"]}', size_hint_y=None, height=40)
            )

            countValue = 0
            if word['id'] in obj.keys():
                countValue = obj[word['id']]

            row.add_widget(
                Label(text=str(countValue), size_hint_y=None, height=40)
            )

            btn = Button(
                text=f'delete',
                size_hint_y=None,
                height=40,
                on_press=self.deleteCb
            )
            btn.rowId = word['id']
            btn.word = word['word']

            row.add_widget(btn)
            self.add_widget(row)

    def deleteCb(self, inst):

        self.popup = Popup(
            title='are you sure you want to delete {}'.format(inst.word),
            size_hint=(None, None),
            size=(400, 200),
        )

        g = GridLayout()
        g.rows = 1

        delBtn = Button(
            text='Delete',
            on_press=lambda i: self.deleteWord([inst.rowId])  # noqa E501
        )

        g.add_widget(
            delBtn
        )
        g.add_widget(
            Button(
                text="Cancel",
                on_press=self.popup.dismiss
            )
        )

        self.popup.content = g
        self.popup.open()

    def deleteWord(self, rowId: list):
        Word().removeById(rowId)
        self.popup.dismiss()
        self.buildList()
