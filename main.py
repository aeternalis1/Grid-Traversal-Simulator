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

Config.set('input','mouse','mouse,multitouch_on_demand')
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')
Config.set('graphics','resizable',False)


class node:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.wall = 0

#width and height of window allocated to grid (rest for commands)
w_width = 900
w_height = 600-(600/10)

#number of rows and columns
width = 50
height = 30

grid = [[] for x in range(height)]

#scale block sizes to fit window
sz = 18

for i in range(height):
    for j in range(width):
        grid[i].append(node(j*sz,i*sz))


class mainApp(App):
    def build(self):
        layout = FloatLayout()
        with layout.canvas:
            for i in range(height):
                for j in range(width):
                    Rectangle(pos=(grid[i][j].x,grid[i][j].y),size=(sz-1,sz-1))
        return layout

glApp = mainApp()

if __name__=='__main__':
    glApp.run()