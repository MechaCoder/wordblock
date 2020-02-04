from kivy.uix.button import Button
from kivy.uix.popup import Popup


def popUp(msg: str = '', autoDismiss: bool=True):

    popObj = Popup(
        title=msg,
        size_hint=(None, None),
        size=(200, 200),
        auto_dismiss=autoDismiss
    )
    popObj.content = Button(
        text='Dismiss',
        on_press=popObj.dismiss
    )
    popObj.open()
    return True
