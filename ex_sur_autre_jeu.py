try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox

from sokobanXSBLevels import *
from enum import Enum

"""
Direction :
    Utile pour gérer le calcul des positions pour les mouvements
"""
class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

"""
Position :
    - stockage de coordoannées x et y,
    - vérification de x et y par rapport à une matrice
    - calcule de position relative à partir d'un offset (un décalage) et une direction
"""
class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Position(' + str(self.x) + ',' + str(self.y) + str(')')

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    # retoune la position vers la direction #direction en tenant compte de l'offset
    #   Position(3,4).positionTowards(Direction.Right, 2) == Position(5,4)
    def positionTowards(self, direction, offset):
        " a compléter "

    # Retourne True si les coordonnées sont valides dans le wharehouse
    def isValidInWharehouse(self, wharehouse):
        return wharehouse.isPositionValid(self)

    # Convertit le receveur en une position correspondante dans un Canvas
    def asCanvasPositionIn(self, elem):
        lx = self.getX() * elem.getWidth()
        ly = self.getY() * elem.getHeight()
        return Position(lx, ly)

"""
WharehousePlan : Plan de l'entrepot pour stocker les éléments.
    Les éléments sont stockés dans une matrice (#rawMatrix)
"""
class WharehousePlan(object):
    def __init__(self):
        # la matrice d'Elem
        self.rawMatrix = []

    def appendRow(self, row):
        self.rawMatrix.append(row)

    def at(self, position):
        x, y = position.getX(), position.getY()
        if 0 <= y < len(self.rawMatrix) and 0 <= x < len(self.rawMatrix[y]):
            return self.rawMatrix[y][x]
        return None

    def atPut(self, position, elem):
        x, y = position.getX(), position.getY()
        if 0 <= y < len(self.rawMatrix) and 0 <= x < len(self.rawMatrix[y]):
            self.rawMatrix[y][x] = elem

    def isPositionValid(self, position):
        return self.at(position) is not None

    def hasFreePlaceAt(self, position):
        elem = self.at(position)
        return elem is not None and elem.isFreePlace()

    def asXsbMatrix(self):
        return xsbMatrix(self.rawMatrix)
    
class Level(object):
    def __init__(self, root, xsbMatrix):
        self.root = root
        self.wharehouse = WharehousePlan()

        # calcul des dimensions de la matrice
        nbrows = len(xsbMatrix)
        nbcolumns = 0

        for line in xsbMatrix:
            nbc = len(line)
            if nbc > nbcolumns:
                nbcolumns = nbc

        self.height = nbrows * 64
        self.width = nbcolumns * 64
 
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="gray")
        self.canvas.pack()

        self.initWharehouseFromXsb(xsbMatrix, nbrows, nbcolumns)
        #self.root.bind("<Key>", self.keypressed)

    def initWharehouseFromXsb(self,xsbMatrix, nbrows, nbcolumns):
        self.matrix = []
        for lineIdx in range(nbrows):
            self.matrix.append([])
            for elemIdx in range(nbcolumns):
                self.matrix[lineIdx].append(None)

        y = 0
        for lineIdx in range(len(xsbMatrix)):
            x = 0
            for elemIdx in range(len(xsbMatrix[lineIdx])):
                e = xsbMatrix[lineIdx][elemIdx]
                if e == '#':
                    self.matrix[y][x] = tk.PhotoImage(file='wall.png')
                    self.canvas.create_image(x*64, y*64, image=self.matrix[y][x], tag="static")
                elif e == '@':
                    self.matrix[y][x] = tk.PhotoImage(file='playerDown.png')
                    self.playerId = self.canvas.create_image(x*64, y*64, image=self.matrix[y][x], tag="static")
                    self.playerX = x
                    self.playerY = y
                elif e == '$':
                    self.matrix[y][x] = tk.PhotoImage(file='box.png')
                    self.canvas.create_image(x*64, y*64, image=self.matrix[y][x], tag="static")
                elif e == '.':
                    self.matrix[y][x] = tk.PhotoImage(file='goal.png')
                    self.canvas.create_image(x*64, y*64, image=self.matrix[y][x], tag="static")
                elif e == '*':
                    self.matrix[y][x] = tk.PhotoImage(file='boxOnTarget.png')
                    self.canvas.create_image(x*64, y*64, image=self.matrix[y][x], tag="static")
                else:
                    None
                x = x + 1
            y = y + 1
            x = 0
        self.canvas.tag_raise("movable","static")
        
    #def keypressed(self, event):
        

class Sokoban(object):
    '''
    Main Level class
    '''

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Sokoban")
        print('Sokoban: ' + str(len(SokobanXSBLevels)) + ' levels')
        self.level = Level(self.root, SokobanXSBLevels[99])
        #self.level = Level(self.root, [
            #['-','-','$','+','$','.','-','.','.','.','.','-','-','.','.','-','-','.','-'] ])
        #self.level = Level(self.root, [ ['@'] ])
 
    def play(self):
        self.root.mainloop()


Sokoban().play()