from TileMap import *
from constants import *
from Coordinates import *
from Global_image_load import *

class Unit:
    def __init__(self,position,lettre,cout,hp,temps_entrainement,attaque,vitesse):
        self.lettre=lettre
        self.position=position
        self.cout=cout
        self.hp=hp
        self.temps_entrainement=temps_entrainement
        self.attaque=attaque
        self.vitesse=vitesse

        self.map_data = map_data
        self.tile_map = TileMap()
        self.coordinates = Coordinates()

        self.frame_index = 0 # indice du frame dans une ligne
        self.direction_index = 0 # indice du frame dans une colonne
        self.last_time = pygame.time.get_ticks() # dernier moment du sprite (dernière action)
    
    def animation(self,current_time):  # fonction qui modifie l'indice des frames et le dernier temps du frame
        if current_time - self.last_time > 1000//30: #1000//30: 30 frames par 1000 millisecondes
            self.last_time = current_time
            self.frame_index = (self.frame_index + 1) % 30
            #self.direction_index=(self.direction_index + 1) % 16

    def frame_coordinates(self,unit_image):
        #calcul des tailles du chaque frame en divisant la taille de l'image principal par le nombre des frames 
        frame_width = unit_image.get_width()//30 #30 nombre des frames par lignes 
        frame_height = unit_image.get_height()//16 #16 nombre des frames par colonnes

        #multiplication de l'indice du frame par la taille de chaque frame pour chercher les vrai coordonnees
        frame_x = self.frame_index * frame_width 
        frame_y = self.direction_index * frame_height

        return frame_x, frame_y, frame_width, frame_height

    def movement(self,cam_x,cam_y):
        while self.coordinates.x>=-5 and self.coordinates.y<=3: # -5 and 3 to stop the unit
            self.coordinates.x-=0.04
            self.coordinates.y+=0.04
            niso_x,niso_y=self.coordinates.to_iso(cam_x,cam_y)
            return niso_x, niso_y
            
    
    def diplay_unit(self, cam_x, cam_y, current_time):
        #coordonnées isométrique    
        iso_x, iso_y = self.coordinates.to_iso(cam_x, cam_y)
        
        #appel de la fonction de l'animation
        self.animation(current_time)

        #appel de la fonction frame_coordinates
        frame_x,frame_y, frame_width, frame_height = self.frame_coordinates(h_man1)

        #enlever un frame de l'image principal et l'afficher a la fois
        frame_rect = pygame.Rect(frame_x,frame_y, frame_width, frame_height)
        unit_frame =  h_man1.subsurface(frame_rect)

        DISPLAYSURF.blit(unit_frame,(iso_x,iso_y))
        self.movement(cam_x,cam_y)
           