import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.spinner import Spinner


class Select(BoxLayout):
    def spinner_clicked(self,value):
        print (value)


class test3App(App):
    def build(self):
        parent = Widget()
        layout = Select()
        parent.add_widget(layout)
        return parent

glApp = test3App()

if __name__=='__main__':
    glApp.run()