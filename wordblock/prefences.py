from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.switch import Switch

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from .data import Prefences

class PrefencesGui(GridLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2

        self.pref = Prefences()
        # speakVal = self.pref.get('speak')['val']
        getSetting = lambda settingName: self.pref.get(settingName)['val']

        # App will speak pref
        ch = Switch(active=getSetting('speak'))
        ch.bind(active=self.callback)
        self.add_widget(Label(text='app will speak words'))
        self.add_widget(ch)

        chMakeCaps = Switch(active=getSetting('makeCaps'))
        chMakeCaps.bind(active=self.callbackMakeCaps)
        self.add_widget(Label(text='app will show all words in Caps'))
        self.add_widget(chMakeCaps)


    def callback(self, inst, value):
        self.pref.set('speak', value)

    def callbackMakeCaps(self, inst, value):
        self.pref.set('makeCaps', value)
