import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ToggleButtonBehavior

li = [0,1,0,0]


class Select(GridLayout):
    check1 = ObjectProperty(True)
    check2 = ObjectProperty(False)
    check3 = ObjectProperty(False)
    check4 = ObjectProperty(False)
    def checked1(self,instance,value):
        if value:
            print ("CHECK1")
    def checked2(self,instance,value):
        if value:
            print ("CHECK2")
    def checked3(self,instance,value):
        if value:
            print ("CHECK3")
    def checked4(self,instance,value):
        if value:
            print ("CHECK4")



class mainApp(App):
    def build(self):
        parent = Widget()
        layout = Select()
        parent.add_widget(layout)
        return parent

glApp = mainApp()

glApp.run()