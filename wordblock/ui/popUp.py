from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

def popUp(msg:str = ''):

    popObj = Popup(
        title=msg,
        size_hint=(None, None),
        size=(200, 200),
    )
    popObj.content = Button(
        text='Dismiss',
        on_press=popObj.dismiss
    )
    popObj.open()
    return True