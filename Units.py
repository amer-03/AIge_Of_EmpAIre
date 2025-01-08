from constants import *
from Coordinates import Coordinates
from Global_image_load import *
import math
import time


class Units:
    """Classe gérant les unités."""

    def __init__(self,image, position,lettre,cout,hp,temps_entrainement,attaque,range,vitesse):
        self.image=image
        self.position=position
        self.lettre=lettre
        self.cout=cout
        self.hp=hp
        self.temps_entrainement=temps_entrainement
        self.attaque=attaque
        self.range=range
        self.vitesse=vitesse

        self.frame_index = 0 # indice du frame dans une ligne
        self.direction_index = 8 # indice du frame dans une colonne
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

    def movement(self,nposition,cam_x,cam_y):
        while self.position.x<nposition.x and self.position.y<nposition.y:
            self.position.x-=0.04
            self.position.y+=0.04
            niso_x,niso_y=self.position.to_iso(cam_x,cam_y)
            return niso_x, niso_y
            
    def diplay_unit(self, cam_x, cam_y, current_time):             
        #coordonnées isométrique    
        iso_x, iso_y = self.position.to_iso(cam_x, cam_y)
                    
        #appel de la fonction de l'animation
        self.animation(current_time)

        #appel de la fonction frame_coordinates
        frame_x,frame_y, frame_width, frame_height = self.frame_coordinates(self.image)

        #enlever un frame de l'image principal et l'afficher a la fois
        frame_rect = pygame.Rect(frame_x,frame_y, frame_width, frame_height)
        self_frame =  self.image.subsurface(frame_rect)

        DISPLAYSURF.blit(self_frame,(iso_x,iso_y))
        #self.movement(Coordinates(-3,3),cam_x,cam_y)

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, other, damage):
        self.hp -= damage
        print(f"{self.lettre} attacks {other.lettre} for {self.attaque} damage. {other.lettre} has {other.hp} HP left.")

    def distance_to(self, other):
        return math.sqrt((Coordinates.to_tuple(self.position)[0] - Coordinates.to_tuple(other.position)[0]) ** 2 + (Coordinates.to_tuple(self.position)[1] - Coordinates.to_tuple(other.position)[1]) ** 2)
    
    def attack(self, other, image):
        while self.is_alive() and other.is_alive():            
            # Unit 1 moves or attacks
            if self.distance_to(other) <= self.range:
                self.take_damage(other, other.attaque)
            if other.distance_to(self) <= other.range:
                other.take_damage(self, self.attaque)
        
        if not self.is_alive():
            self.image=image
            
        elif not other.is_alive():
            other.image=image
        
        #time.sleep(1)  # Pause for better visualization
    def attack_building(self, building):
        while self.is_alive() and building.hp > 0:
            if self.distance_to(building) <= self.range:
                # L'unité inflige des dégâts au bâtiment
                building.hp -= self.attaque
                print(f"{self.lettre} attacks {building.letter} for {self.attaque} damage. {building.letter} has {building.hp} HP left.")
            
            # Attente pour simuler un délai entre les attaques
            time.sleep(1)

        if building.hp <= 0:
            # Le bâtiment est détruit, on supprime l'image du bâtiment (ou on la remplace par une image vide)
            building.image = None
            print(f"{building.letter} has been destroyed!")