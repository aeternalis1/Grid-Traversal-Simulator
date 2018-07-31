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


Config.set('input','mouse','mouse,multitouch_on_demand')
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')


class TouchInput(Widget):
    def on_touch_down(self, touch):
        print (touch)


class node:
    def __init__(self,x,y,hori,vert):
        self.x = x
        self.y = y
        self.hori = hori
        self.vert = vert
        self.col = 0

#width and height of window allocated to grid (rest for commands)
w_width = 900
w_height = 600-(600/10)

#number of rows and columns
width = 50
height = 30

grid = [[None for x in range(width)] for x in range(height)]

#scale block sizes to fit window
hori = w_width//width
vert = w_height//height

for i in range(height):
    for j in range(width):
        grid[i][j] = (node(j*hori,i*vert,hori-1,vert-1))


colours = [(1,1,1,1),(0,0,0,1)]

#change node colour
def paint(x,y,colour,self):
    hori = grid[0][0].hori
    vert = grid[0][0].vert
    gridx = int(x//(hori+1))
    gridy = int(y//(vert+1))
    if gridy>=(len(grid)) or gridx >= len(grid[0]) or gridy < 0 or gridx < 0 or grid[gridy][gridx].col==colour:
        return
    with self.canvas:
        grid[gridy][gridx].col = colour
        Color(*colours[colour])
        Rectangle(pos=(grid[gridy][gridx].x, grid[gridy][gridx].y), size=(hori, vert))
    return


class Touch(Widget):

    def on_touch_down(self, touch):
        x = touch.x
        y = touch.y
        paint(x,y,1,self)

    def on_touch_move(self, touch):
        x = touch.x
        y = touch.y
        paint(x,y,1,self)


class mainApp(App):
    def build(self):
        parent = Widget()
        layout = Touch()
        with layout.canvas:
            Color(.501,.501,.501,1)
            Rectangle(pos=(0,0),size=(900,600))
            Color(1,1,1,1)
            for i in range(30):
                for j in range(50):
                    Rectangle(pos=(grid[i][j].x, grid[i][j].y), size=(grid[i][j].hori, grid[i][j].vert))
        parent.add_widget(layout)
        return parent


glApp = mainApp()

if __name__=='__main__':
    glApp.run()