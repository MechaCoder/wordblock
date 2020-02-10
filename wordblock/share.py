from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from share import Share

class ShareBox(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.cols = 2

        self.snapShot = Button(
            text='SnapShot Words',
            on_press=self.snapshotEvent
        )

        self.add_widget(self.snapShot)
        

    def snapshotEvent(self, inst):
        Share().mkFile()
        print('file made')

    def loadEvent(self, inst):
        pass
        
