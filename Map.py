import random

class Map(object):
    def __init__ (self,terrain_nature,ressource,player_position):
        self.grid=[]
        self.size=120
        self.terrain_nature=terrain_nature
        self.ressource=ressource
        self.player_position=player_position
    
    def generate_map(self):
        for _ in range (self.size):
            self.grid.append([])
        
