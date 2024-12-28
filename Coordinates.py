from constants import *

class Coordinates:
    """Classe gérant les coordonnées."""

    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def __hash__(self):
        return hash((self.x,self.y))

    def __str__(self):
        return f"Position: {self.x},{self.y}"
    
    def to_iso(self,cam_x,cam_y):
        iso_x = (int(self.y - self.x)) * tile_grass.width - cam_x
        iso_y = (int(self.x + self.y)//2) * tile_grass.height - cam_y
        return iso_x,iso_y
    
