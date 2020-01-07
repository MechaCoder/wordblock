from kivy.config import Config
from kivy.core.window import Window
from wordblock import WordBlock


if __name__ == '__main__':
    Window.size = (1500, 300)
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    WordBlock().run()
