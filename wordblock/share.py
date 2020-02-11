from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from share import Share
from .ui.popUp import popUp


class ShareFileLoad(FileChooserIconView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = './'
        self.filters = '[words-*.words.json]'


class ShareBox(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2

        self.snapShot = Button(
            text='SnapShot Words',
            on_press=self.snapshotEvent
        )

        self.loadBtn = Button(
            text='load file',
            on_press=self.loadEvent
        )

        self.add_widget(self.snapShot)
        self.add_widget(self.loadBtn)

    def snapshotEvent(self, inst):
        filename = Share().mkFile()
        popUp(f'all words have been imported {filename}')

    def loadEvent(self, inst):

        self.popup = Popup(
            title="Select File",
            size_hint=(None, None),
            size=(800, 300)
        )

        box = GridLayout()
        box.cols = 1

        self.filelocation = ShareFileLoad()
        self.filelocation.on_submit = self.on_selectEvent

        box.add_widget(self.filelocation)
        box.add_widget(
            Button(
                text='Cancil',
                on_press=self.popup.dismiss,
                size_hint_y=None,
                height=30))

        self.popup.content = box
        self.popup.open()

    def on_selectEvent(self, sel, touch):
        self.popup.dismiss()
        # self.filelocation.selection = sel

        for file in sel:
            # check the name convetion
            fileName = file.split('/')[-1]

            if fileName[:6] != 'words-':
                continue

            if fileName[12:] != '.words.json':
                continue

            Share().readWordsToDB(file)
        popUp('all words have been imported')
