import random

class Map(object):
    def __init__ (self,terrain_nature,ressource,player_position):
        self.size=120
        self.grid=[[0 for _ in range(self.size)]for _ in range(self.size)]
        self.terrain_nature=terrain_nature
        self.ressource=ressource
        self.player_position=player_position
    
    def generate_map(self):
        for _ in range (self.size):
            x=random.randrange(0,self.size)
            self.grid[x]=['~' for _ in range(self.size//6)]
            
    def __str__ (self):
        return str(self.grid)

mymap=Map("foret","bois",(0,0))
mymap.generate_map()
print(mymap)


        



        
