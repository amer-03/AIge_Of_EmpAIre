from TileMap import *
from constants import *
from Coordinates import *

class Unit:
    def __init__(self):
        self.map_data = map_data
        self.tile_map = TileMap()
        self.coordinates = Coordinates()

        self.frame_index = 0 # indice du frame dans une ligne
        self.direction_index = 0 # indice du frame dans une colonne
        self.last_time = pygame.time.get_ticks()
    
    def animation(self,current_time):
        if current_time - self.last_time > 5000//30: #1000//30: 30 sous-images par 1000 millisecondes
            self.last_time = current_time
            self.frame_index = (self.frame_index + 1) % 30
    
    def diplay_unit(self, cam_x, cam_y, current_time):
        unit_tile="images/img_3.webp"

        #coordonnées isométrique    
        iso_x, iso_y = self.coordinates.to_iso(cam_x, cam_y)
        f"iso_x: {iso_x}, iso_y: {iso_y}"

        unit_image=  pygame.image.load(unit_tile).convert_alpha()
        
        self.animation(current_time)
        
        frame_width = unit_image.get_width()//30 #30 nombre des sous images par lignes 
        frame_height = unit_image.get_height()//16 #16 nombre des sous images par colonnes
        f"frame_width: {frame_width}, frame_width: {frame_height}"

        #multiplication de l'indice du frame par la taille de chaque sous image pour chercher le vrai
        frame_x = self.frame_index * frame_width 
        frame_y = self.direction_index * frame_height
        f"frame_x: {frame_x}, frame_y: {frame_y}"
        f"frame_index: {self.frame_index}, direction_index: {self.direction_index}"

        frame_rect = pygame.Rect(frame_x,frame_y, frame_width, frame_height)
        unit_sub_images =  unit_image.subsurface(frame_rect)
        DISPLAYSURF.blit(unit_sub_images,(iso_x,iso_y))
        
unit=Unit()
unit.diplay_unit(4,4,pygame.time.get_ticks())

        




    

                    