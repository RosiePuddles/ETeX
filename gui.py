from LaTeX import *
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

Doc = Document()
genericBox = AnchorLayout(padding=10)
button = Button(text='My first button')
genericBox.add_widget(button)


class MainScreen(AnchorLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.button = Button(text='My first button')
        genericBox.add_widget(self.button)


class MyApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
