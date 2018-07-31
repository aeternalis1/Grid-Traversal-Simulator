import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.graphics import *
from kivy.uix.widget import Widget


class TouchInput(Widget):
    def on_touch_down(self, touch):
        print (touch.x,touch.y)
    def on_touch_move(self, touch):
        print (touch)


class mainApp(App):
    def build(self):
        return TouchInput()

glApp = mainApp()

glApp.run()