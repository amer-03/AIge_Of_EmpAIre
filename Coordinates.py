from TileMap import *
from constants import *

class Coordinates:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def to_iso(self,cam_x,cam_y):
        iso_x = (int(self.y - self.x)) * tile_grass.width - cam_x
        iso_y = (int(self.x + self.y)//2) * tile_grass.height - cam_y
        return iso_x,iso_y