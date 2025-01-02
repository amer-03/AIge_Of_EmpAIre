from Units import Units
import time
from TileMap import TileMap
from Coordinates import Coordinates
from Villager import Villager
from Swordman import Swordman
from Archer import Archer
from Horseman import Horseman
from Global_image_load import *
from constants import *
import pygame
from pygame.locals import *

class Test:
    def __init__(self):
        self.scroll_speed = 30
        self.tile_map = TileMap()
        self.villager = Villager(villager1,Coordinates(0,0))
        self.villager2 = Villager(villager3,Coordinates(-2,5))
        self.swordman = Swordman(s_man1,Coordinates(3,3))  
        self.horseman = Horseman(h_man1,Coordinates(-3,-3))  
        self.archer = Archer(archer1,Coordinates(-6,-6))
        self.archer2 = Archer(archer2,Coordinates(3,-5)) 
         
        self.tiles={}
    
        self.tile_map.add_unit(self.villager,Villager,4,1,self.tiles)  
        self.tile_map.add_unit(self.villager2,Villager,2,1,self.tiles)   
        self.tile_map.add_unit(self.horseman,Horseman,6,1,self.tiles)   
        self.tile_map.add_unit(self.archer,Archer,3,1,self.tiles)   
        self.tile_map.add_unit(self.archer2,Archer,3,1,self.tiles)   
        self.tile_map.add_unit(self.swordman,Swordman,4,1,self.tiles)

        assert self.tiles!={}, "units not added"

        self.tile_map.add_wood_patches()
        self.tile_map.add_gold_middle()

    def center_camera_on_tile(self):
        center_x = size // 2
        center_y = size // 2
        cart_x = center_x * tile_grass.width_half
        cart_y = center_y * tile_grass.height_half
        iso_x = (cart_x - cart_y)
        iso_y = (cart_x - cart_y) // 2
        cam_x = (iso_x - screen_width // 2) + tile_grass.width_half
        cam_y = -(iso_y + screen_height // 2)
        return cam_x, cam_y
    
        
    def calculate_camera_limits(self):
        """Calcule les limites de la caméra pour empêcher le défilement hors de la carte."""
        # Taille de la moitié de la carte

        # Calcul des coins en coordonnées cartésiennes
        min_cart_x = -half_size * tile_grass.width_half
        max_cart_x = half_size * tile_grass.width_half
        min_cart_y = -half_size * tile_grass.height_half
        max_cart_y = half_size * tile_grass.height_half

        # Conversion des coins en isométriques
        min_iso_x = min_cart_x - max_cart_y
        max_iso_x = max_cart_x - min_cart_y
        min_iso_y = (min_cart_x + min_cart_y) // 2
        max_iso_y = (max_cart_x + max_cart_y) // 2

        # Ajustement pour la taille de l'écran
        min_cam_x = min_iso_x - (screen_width // 2) + screen_width // 2 + (-5 * tile_grass.width_half)
        max_cam_x = max_iso_x - (screen_width // 2) - screen_width // 2 + 5 * tile_grass.width_half
        min_cam_y = min_iso_y - (screen_height // 2) + screen_height // 2 + (-5 * tile_grass.width_half)
        max_cam_y = max_iso_y - (screen_height // 2) - screen_height // 2 + 5 * tile_grass.width_half

        return min_cam_x, min_cam_y, max_cam_x, max_cam_y
    
    def handle_camera_movement(self, keys):
        min_cam_x, min_cam_y, max_cam_x, max_cam_y = self.calculate_camera_limits()
        speed = self.scroll_speed * 2 if keys[K_LSHIFT] or keys[K_RSHIFT] else self.scroll_speed
        if keys[K_q]:
            self.cam_x = max(self.cam_x - speed, min_cam_x)  # Déplace à gauche
        if keys[K_d]:
            self.cam_x = min(self.cam_x + speed, max_cam_x)  # Déplace à droite
        if keys[K_z]:
            self.cam_y = max(self.cam_y - speed, min_cam_y)  # Déplace vers le haut
        if keys[K_s]:
            self.cam_y = min(self.cam_y + speed, max_cam_y)  # Déplace vers le bas

        def draw_map_in_terminal(self, stdscr):
            self.init_player_colors()
            stdscr.clear()
            stdscr.nodelay(1)
            stdscr.timeout(500)

            max_rows, max_cols = stdscr.getmaxyx()
            map_rows = size
            map_cols = size

            while self.terminal_active:
                stdscr.clear()

                player_x, player_y = self.tile_map.position_initiale
                view_top = max(0, min(player_x - max_rows // 2, map_rows - max_rows))
                view_left = max(0, min(player_y - max_cols // 2, map_cols - max_cols))

                for row in range(view_top, min(view_top + max_rows, map_rows)):
                    for col in range(view_left, min(view_left + max_cols, map_cols)):

                        if (row, col) == (player_x, player_y):
                            #print(curses.color_pair(1))
                            stdscr.addstr(row - view_top, col - view_left, "P",
                                        curses.color_pair(1))  # Rouge pour le joueur
                        else:

                            tile = tuiles.get((row, col), {})
                            char = " "  # Espace vide par défaut
                            color = 0  # Pas de couleur par défaut

                            # Déterminer le caractère à afficher pour cette tuile

                            if "batiments" in tile:
                                for joueur, batiments_joueur in tile["batiments"].items():
                                    #print(row, col ,batiments_joueur)
                                    for batiment_type, details in batiments_joueur.items():

                                        if batiment_type == "T":
                                            char = "T"
                                            color = self.get_player_color(joueur)
                                        elif batiment_type == "H":
                                            char = "H"
                                            color = self.get_player_color(joueur)
                                        elif batiment_type == "C":
                                            char = "C"
                                            color = self.get_player_color(joueur)
                                        elif batiment_type == "F":
                                            char = "F"
                                            color = self.get_player_color(joueur)
                                        elif batiment_type == "B":
                                            char = "B"
                                            color = self.get_player_color(joueur)
                                        elif batiment_type == "S":
                                            char = "S"
                                            color = self.get_player_color(joueur)
                                        elif batiment_type == "A":
                                            char = "A"
                                            color = self.get_player_color(joueur)
                                        elif batiment_type == "K":
                                            char = "K"
                                            color = self.get_player_color(joueur)
                                        else :
                                            char = " "
                                        break
                                    break


                            elif "unites" in tile:
                                for joueur, unites_joueur in tile["unites"].items():
                                    for unite_type, details in unites_joueur.items():
                                        if unite_type == "v":
                                            char = "v"
                                            color = self.get_player_color(joueur)
                                            #print(color)
                                        elif unite_type == "a":
                                            char = "a"
                                            color = self.get_player_color(joueur)
                                        elif unite_type == "h":
                                            char = "h"
                                            color = self.get_player_color(joueur)
                                        elif unite_type == "s":
                                            char = "s"
                                            color = self.get_player_color(joueur)
                                        else :
                                            char = " "

                                        break
                                    break

                            # Déterminer les ressources
                            elif "ressources" in tile:
                                ressource = tile["ressources"]
                                if ressource == "G":
                                    char = "G"
                                elif ressource == "W":
                                    char = "W"
                                else:
                                    char = " "
                            if color != 0:
                                stdscr.addstr(row - view_top, col - view_left, char,
                                            color)
                            else:
                                stdscr.addstr(row - view_top, col - view_left, char)  # Pas de couleur
                stdscr.refresh()


                # Gestion des touches pour déplacer le joueur
                key = stdscr.getch()  # Attendre une touche
                if key == ord('q'):  # Haut
                    self.tile_map.move_player('up')
                elif key == ord('d'):  # Bas
                    self.tile_map.move_player('down')
                elif key == ord('z'):  # Gauche
                    self.tile_map.move_player('left')
                elif key == ord('s'):  # Droite
                    self.tile_map.move_player('right')

                elif key == ord('p'):
                    self.ouvrir_terminal()

                time.sleep(0.1)
     
    def run(self):
        cam_x,cam_y=self.center_camera_on_tile()
        running=True
        while running:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    running=False

            DISPLAYSURF.fill(BLACK)

            # affichage iso de la map
            self.tile_map.display_map(cam_x, cam_y)  

            #affichage des unités          
            for position,players in self.tiles.items():
                for player,units in players.items():
                    for unit in units:
                        unit.diplay_unit(cam_x,cam_y,pygame.time.get_ticks())

            # affichage de la carte dans un terminal
            with open("map.txt","w") as file:
                for i in range(len(map_data)):
                   for j in range(len(map_data[i])):
                        file.write(map_data[i][j])

            fps = int(FPSCLOCK.get_fps())
            fps_text = pygame.font.Font(None, 24).render(f"FPS: {fps}", True, (255, 255, 255))
            DISPLAYSURF.blit(fps_text, (10, 10))
            #print(fps)

            pygame.display.update()
            pygame.display.flip()
            FPSCLOCK.tick(600)
            # print(self.tiles)        