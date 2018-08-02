import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.slider import Slider
from random import randint
from random import shuffle
from functools import partial


Config.set('input','mouse','mouse,multitouch_on_demand')
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)


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
backtrack = [[[-1,-1] for x in range(width)] for x in range(height)]

#scale block sizes to fit window
hori = w_width//width
vert = w_height//height

for i in range(height):
    for j in range(width):
        grid[i][j] = (node(j*hori,i*vert,hori-1,vert-1))

colours = [(0,0,0,1),(0,1,0,1),(1,0,0,1),(1,1,1,1)]
colour = [0]
walls = ["Wall","Source","Target","Blank"]


moves = [[1,0],[0,1],[-1,0],[0,-1]]
algo = [0]
algos = ["BFS","DFS"]
running = [0]
speed = [50]


queue = []
stack = [0 for x in range(width*height)]
queueInd = [0,0]
stackInd = [0]


#change node colour
def paint(x,y,self):
    hori = grid[0][0].hori
    vert = grid[0][0].vert
    gridx = int(x//(hori+1))
    gridy = int(y//(vert+1))
    if gridy>=(len(grid)) or gridx >= len(grid[0]) or gridy < 0 or gridx < 0:
        return
    with self.canvas:
        grid[gridy][gridx].col = colour[0]
        Color(*colours[colour[0]])
        Rectangle(pos=(grid[gridy][gridx].x, grid[gridy][gridx].y), size=(hori, vert))
    return


def resetGrid(self):
    self.canvas.clear()
    with self.canvas:
        Color(.501,.501,.501,1)
        Rectangle(pos=(0,0),size=(900,540))
        for i in grid:
            for j in i:
                Color(*colours[j.col])
                Rectangle(pos=(j.x,j.y),size=(j.hori,j.vert))
    self.clear_widgets()
    self.add_widget(Touch())
    tools = ToolBar()
    tools.ids.spinner_id.text = walls[colour[0]]
    tools.ids.spinner_id2.text = algos[algo[0]]
    self.add_widget(tools)
    select = speedSelect(value=speed[0])
    select.update()
    self.add_widget(select)


def runPath(self,*largs):
    if not running[0]:
        stackInd[0] = -1
    if stackInd[0]<0:
        return
    y,x = stack[stackInd[0]]
    stackInd[0] -= 1
    if grid[y][x].col != 1:
        with self.canvas:
            Color(0,0,1,1)
            Rectangle(pos=(grid[y][x].x, grid[y][x].y), size=(grid[y][x].hori, grid[y][x].vert))
    Clock.schedule_once(partial(runPath,self),(101-speed[0])/200)


def bfsUpdate(self,*largs):
    for i in range(len(queue)):
        y,x = queue.pop(0)
        if grid[y][x].col==2:
            while queue:
                queue.pop(-1)
            stackInd[0] = -1
            while backtrack[y][x] != [-1, -1]:
                stackInd[0] += 1
                stack[stackInd[0]] = backtrack[y][x]
                y, x = backtrack[y][x]
            Clock.schedule_once(partial(runPath, self), (101-speed[0])/200)
            return
        if grid[y][x].col != 1:
            with self.canvas:
                Color(0,1,1,1)
                Rectangle(pos=(grid[y][x].x, grid[y][x].y), size=(grid[y][x].hori, grid[y][x].vert))
        for j in moves:
            ny,nx = y+j[0],x+j[1]
            if ny < 0 or ny >= height or nx < 0 or nx >= width:
                continue
            if grid[ny][nx].col == 0 or checked[ny][nx]:
                continue
            checked[ny][nx] = 1
            backtrack[ny][nx] = [y,x]
            queue.append([ny,nx])
    Clock.schedule_once(partial(bfsUpdate,self),(101-speed[0])/200)


def bfs(self,*largs):
    while queue:
        queue.pop(-1)
    height,width = len(grid),len(grid[0])
    for i in range(height):
        for j in range(width):
            checked[i][j] = 0
            if grid[i][j].col==1:
                queue.append([i,j])
                checked[i][j] = 1
            backtrack[i][j] = [-1,-1]
    if queue:
        bfsUpdate(self)


def dfsUpdate(self,*largs):
    if not queue or not running[0]:
        return
    y,x = queue.pop(-1)
    if grid[y][x].col==2:
        while queue:
            queue.pop(-1)
        stackInd[0] = -1
        while backtrack[y][x] != [-1,-1]:
            stackInd[0] += 1
            stack[stackInd[0]] = backtrack[y][x]
            y,x = backtrack[y][x]
        Clock.schedule_once(partial(runPath,self),(101-speed[0])/200)
        return
    if grid[y][x].col != 1:
        with self.canvas:
            Color(0,1,1,1)
            Rectangle(pos=(grid[y][x].x, grid[y][x].y), size=(grid[y][x].hori, grid[y][x].vert))
    shuffle(moves)
    for i in moves:
        ny,nx = y+i[0],x+i[1]
        if ny < 0 or ny >= height or nx < 0 or nx >= width:
            continue
        if grid[ny][nx].col == 0 or checked[ny][nx]:
            continue
        queue.append([ny,nx])
        backtrack[ny][nx] = [y,x]
        checked[ny][nx] = 1
    Clock.schedule_once(partial(dfsUpdate,self),(101-speed[0])/200)


def dfs(self,*largs):
    if not running[0]:
        return
    while queue:
        queue.pop(-1)
    height,width = len(grid),len(grid[0])
    for i in range(height):
        for j in range(width):
            checked[i][j] = 0
            backtrack[i][j] = [-1,-1]
    for i in range(height):
        for j in range(width):
            if grid[i][j].col==1:
                checked[i][j] = 1
                queue.append([i, j])
    if queue:
        dfsUpdate(self)


class Touch(Widget):

    def on_touch_down(self, touch):
        x = touch.x
        y = touch.y
        paint(x,y,self.parent)

    def on_touch_move(self, touch):
        x = touch.x
        y = touch.y
        paint(x,y,self.parent)


class speedSelect(Slider):

    def changeSpeed(self,*args):
        speed[0] = int(args[1])
        self.lbl.text = str(int(args[1]))

    def update(self):
        self.lbl.text = str(speed[0])


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
        if running[0]:
            running[0] = 0
            stackInd[0] = -1
            while queue:
                queue.pop(-1)
        for i in grid:
            for j in i:
                if randint(1,4)==1:
                    j.col = 0
                else:
                    j.col = 3
        y,x = randint(0,len(grid)-1),randint(0,len(grid[0])-1)
        a,b = randint(0,len(grid)-1),randint(0,len(grid[0])-1)
        while a==y and b==x:
            a, b = randint(0, len(grid) - 1), randint(0, len(grid[0]) - 1)
        grid[y][x].col = 1
        grid[a][b].col = 2
        resetGrid(self.parent)

    def clear(self):
        if running[0]:
            running[0] = 0
            stackInd[0] = -1
            while queue:
                queue.pop(-1)
        for i in grid:
            for j in i:
                j.col = 3
        resetGrid(self.parent)

    def simulate(self):
        while queue:
            queue.pop(-1)
        stackInd[0] = -1
        running[0] = 1
        if algo[0]==0:
            bfs(self.parent)
        else:
            dfs(self.parent)
        resetGrid(self.parent)


class MainApp(App):
    def build(self):
        self.title = "Grid Traversal Simulator"
        parent = Widget()
        layout = Touch()
        tools = ToolBar()
        select = speedSelect(value=speed[0])
        with layout.canvas:
            Color(.501,.501,.501,1)
            Rectangle(pos=(0,0),size=(900,540))
        with layout.canvas:
            Color(1,1,1,1)
            for i in range(30):
                for j in range(50):
                    Rectangle(pos=(grid[i][j].x, grid[i][j].y), size=(grid[i][j].hori, grid[i][j].vert))
        parent.add_widget(layout)
        parent.add_widget(tools)
        parent.add_widget(select)
        return parent


gridsim = MainApp()

if __name__=='__main__':
    gridsim.run()
