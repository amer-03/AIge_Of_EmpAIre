from Units import Units
import time
from TileMap import TileMap
from Coordinates import Coordinates
from Buildings import Buildings
from Villager import Villager
from Swordman import Swordman
from Archer import Archer
from Horseman import Horseman
from TownCenter import TownCenter
from House import House
from ArcheryRange import ArcheryRange
from Camera import Camera
from Global_image_load import *
from constants import *
import pygame
from pygame.locals import *

class Test:
    def __init__(self):
        self.position_init= (size // 2, size // 2)
        self.camera=Camera()
        self.tile_map = TileMap()

        self.villager = Villager(villager1,Coordinates(60,50))
        self.horseman = Horseman(h_man1,Coordinates(60,60))
        
        self.tiles={}
        
        self.tile_map.add_unit(self.villager,Villager,1,1,self.tiles)
        self.tile_map.add_unit(self.horseman,Horseman,1,1,self.tiles)        
                       
        assert self.tiles!={}, "units not added"
        
        self.towncenter1= TownCenter(Tile("images/Town_Center.webp", 200, 128).image,Coordinates(0,20))
        self.towncenter2= TownCenter(Tile("images/Town_Center.webp", 200, 128).image,Coordinates(0,-20))
        
        self.build_tiles={}
        
        self.tile_map.add_building(self.towncenter1,TownCenter,1,1,self.build_tiles)
        self.tile_map.add_building(self.towncenter2,TownCenter,1,2,self.build_tiles)
        
        assert self.build_tiles!={}, "buildings not added"

        self.tile_map.add_wood_patches()
        self.tile_map.add_gold_middle()

    def move_player(self,direction):
        x, y = self.position_init
        if direction == 'u' and y > 0:
            y -= 1
        elif direction == 'd' and y < size - 1:
            y += 1
        elif direction == 'l' and x > 0:
            x -= 1
        elif direction == 'r' and x < size - 1:
            x += 1
        self.position_init = (x, y)

    def run(self):
        running=True
        FPSCLOCK = pygame.time.Clock()
        while running:
            dt=FPSCLOCK.tick(600)/1000
            dt*=5            
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    running=False

            DISPLAYSURF.fill(BLACK)

            #se déplacer dans la map
            self.camera.handle_camera_movement(key)

            if key[pygame.K_z]:  # Haut
                self.move_player('u')
            elif key[pygame.K_s]:  # Bas
                self.move_player('d')
            elif key[pygame.K_q]:  # Gauche
                self.move_player('l')
            elif key[pygame.K_d]:  # Droite
                self.move_player('r')

            # affichage iso de la map
            self.tile_map.display_map(self.camera.cam_x, self.camera.cam_y)
            
            #affichage des buildings
            #for position,players in self.build_tiles.items():
             #   for player,buildings in players.items():
              #      for building in buildings:
               #         building.display_building(self.camera.cam_x, self.camera.cam_y) 
            
            #affichage des unités          
            for position,players in self.tiles.items():
                for player,units in players.items():
                    for unit in units:
                        #unit.attack(unit,villager3)
                        unit.display_unit(self.camera.cam_x, self.camera.cam_y, dt)

            fps = int(FPSCLOCK.get_fps())
            fps_text = pygame.font.Font(None, 24).render(f"FPS: {fps}", True, (255, 255, 255))
            DISPLAYSURF.blit(fps_text, (10, 10))
            #print(fps)

            pygame.display.update()
            pygame.display.flip()
            
            # print(self.tiles)       