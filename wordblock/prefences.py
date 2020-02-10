from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.gridlayout import GridLayout

from .settings import UrlLayout
from .share import ShareBox

from .data import Prefences


class PrefencesGui(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2

        self.pref = Prefences()

        # App will speak pref
        ch = Switch(active=self.getSettingValue('speak'))
        ch.bind(active=self.callback)
        self.add_widget(Label(text='app will speak words'))
        self.add_widget(ch)

        chMakeCaps = Switch(active=self.getSettingValue('makeCaps'))
        chMakeCaps.bind(active=self.callbackMakeCaps)
        self.add_widget(Label(text='app will show all words in Caps'))
        self.add_widget(chMakeCaps)

        self.add_widget(
            Label(text="URL importing")
        )

        self.urlLayout = UrlLayout()
        self.add_widget(self.urlLayout)

        self.add_widget(
            Label(text='import and export btn')
        )
        self.add_widget(ShareBox())

    def callback(self, inst, value):
        self.pref.set('speak', value)

    def callbackMakeCaps(self, inst, value):
        self.pref.set('makeCaps', value)

    def getSettingValue(self, settingName: str):
        return self.pref.get(settingName)['val']
