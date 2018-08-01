import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.clock import Clock
from random import randint
from random import shuffle
from functools import partial


Config.set('input','mouse','mouse,multitouch_on_demand')
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')


class node:
    def __init__(self,x,y,hori,vert):
        self.x = x
        self.y = y
        self.hori = hori
        self.vert = vert
        self.col = 3

#width and height of window allocated to grid (rest for commands)
w_width = 900
w_height = 600-(600/10)

#number of rows and columns
width = 50
height = 30

grid = [[None for x in range(width)] for x in range(height)]
checked = [[0 for x in range(width)] for x in range(height)]

#scale block sizes to fit window
hori = w_width//width
vert = w_height//height

for i in range(height):
    for j in range(width):
        grid[i][j] = (node(j*hori,i*vert,hori-1,vert-1))

colours = [(0,0,0,1),(0,1,0,1),(1,0,0,1),(1,1,1,1)]
colour = [0]

moves = [[1,0],[0,1],[-1,0],[0,-1]]
algo = [0]
queue = []

#change node colour
def paint(x,y,self):
    hori = grid[0][0].hori
    vert = grid[0][0].vert
    gridx = int(x//(hori+1))
    gridy = int(y//(vert+1))
    if gridy>=(len(grid)) or gridx >= len(grid[0]) or gridy < 0 or gridx < 0 or grid[gridy][gridx].col==colour[0]:
        return
    with self.canvas:
        grid[gridy][gridx].col = colour[0]
        Color(*colours[colour[0]])
        Rectangle(pos=(grid[gridy][gridx].x, grid[gridy][gridx].y), size=(hori, vert))
    return

def bfs(self):
    queue = []
    height,width = len(grid),len(grid[0])
    for i in range(height):
        for j in range(width):
            checked[i][j] = 0
            if grid[i][j].col==1:
                queue.append([i,j])
                checked[i][j] = 1
    while queue:
        for j in range(len(queue)):
            y,x = queue.pop(0)
            for i in moves:
                ny,nx = y+i[0],x+i[1]
                if ny < 0 or ny >= height or nx < 0 or nx >= width:
                    continue
                if grid[ny][nx].col==0 or checked[ny][nx]:
                    continue
                checked[ny][nx] = 1
                if grid[ny][nx].col==2:
                    return
                with self.canvas:
                    Color(0,0,1,1)
                    Rectangle(pos=(grid[ny][nx].x, grid[ny][nx].y), size=(grid[ny][nx].hori, grid[ny][nx].vert))
                queue.append([ny,nx])


def dfsUpdate(self,*largs):
    if not queue:
        return
    y,x = queue.pop(-1)
    if grid[y][x].col==2:
        while queue:
            queue.pop(-1)
        return
    checked[y][x] = 1
    with self.canvas:
        Color(0,0,1,1)
        Rectangle(pos=(grid[y][x].x, grid[y][x].y), size=(grid[y][x].hori, grid[y][x].vert))
    shuffle(moves)
    for i in moves:
        ny,nx = y+i[0],x+i[1]
        if ny < 0 or ny >= height or nx < 0 or nx >= width:
            continue
        if grid[ny][nx].col == 0 or checked[ny][nx]:
            continue
        queue.append([ny,nx])
        checked[ny][nx] = 1
        Clock.schedule_once(partial(dfsUpdate,self),1.0/60.0)


def dfs(self):
    while queue:
        queue.pop(-1)
    height,width = len(grid),len(grid[0])
    for i in range(height):
        for j in range(width):
            checked[i][j] = 0
    for i in range(height):
        for j in range(width):
            if grid[i][j].col==1:
                checked[i][j] = 1
                shuffle(moves)
                for k in moves:
                    ny, nx = i + k[0], j + k[1]
                    if ny < 0 or ny >= height or nx < 0 or nx >= width:
                        continue
                    if grid[ny][nx].col == 0 or checked[ny][nx]:
                        continue
                    queue.append([ny, nx])
    if queue:
        print ("HERE")
        print (queue)
        Clock.schedule_once(partial(dfsUpdate,self),1.0/60.0)


class Touch(Widget):

    def on_touch_down(self, touch):
        x = touch.x
        y = touch.y
        paint(x,y,self.parent)
        dfs(self.parent)                 #TEMPORARY FOR TESTING, MAKE SURE TO REMOVE

    def on_touch_move(self, touch):
        x = touch.x
        y = touch.y
        paint(x,y,self.parent)


class ToolBar(BoxLayout):

    def spinner_clicked(self,value):
        if value=='Wall':
            colour[0] = 0
        elif value=='Source':
            colour[0] = 1
        elif value=='Target':
            colour[0] = 2
        elif value=='Blank':
            colour[0] = 3

    def spinner_clicked2(self,value):
        if value=='BFS':
            algo[0] = 0
        else:
            algo[0] = 1

    def randomize(self):
        for i in grid:
            for j in i:
                if randint(1,4)==1:
                    j.col = 0
                else:
                    j.col = 3
                with self.parent.canvas:
                    Color(*colours[j.col])
                    Rectangle(pos=(j.x, j.y), size=(j.hori, j.vert))
        y,x = randint(0,len(grid)-1),randint(0,len(grid[0])-1)
        a,b = randint(0,len(grid)-1),randint(0,len(grid[0])-1)
        while a==y and b==x:
            a, b = randint(0, len(grid) - 1), randint(0, len(grid[0]) - 1)
        grid[y][x].col = 1
        grid[a][b].col = 2
        with self.parent.canvas:
            Color(*colours[1])
            Rectangle(pos=(grid[y][x].x, grid[y][x].y), size=(grid[y][x].hori, grid[y][x].vert))
            Color(*colours[2])
            Rectangle(pos=(grid[a][b].x, grid[a][b].y), size=(grid[a][b].hori, grid[a][b].vert))

    def clear(self):
        for i in grid:
            for j in i:
                j.col = 3
                with self.parent.canvas:
                    Color(*colours[j.col])
                    Rectangle(pos=(j.x, j.y), size=(j.hori, j.vert))

    def simulate(self):
        if algo[0]==0:
            bfs(self.parent)
        else:
            dfs(self.parent)


class testApp(App):
    def build(self):
        parent = Widget()
        layout = Touch()
        tools = ToolBar()
        with parent.canvas:
            Color(.501,.501,.501,1)
            Rectangle(pos=(0,0),size=(900,600))
            Color(1,1,1,1)
            for i in range(30):
                for j in range(50):
                    Rectangle(pos=(grid[i][j].x, grid[i][j].y), size=(grid[i][j].hori, grid[i][j].vert))
        parent.add_widget(tools)
        parent.add_widget(layout)
        return parent


gridsim = testApp()

if __name__=='__main__':
    gridsim.run()