import pygame
#from Player import *
from pygame.locals import *
import sys
import numpy as np
import random
from math import *
import subprocess
import os
import json

pygame.init()

# Configuration de l'écran et des FPS
screen_width = 1920
screen_height = 1080
DISPLAYSURF = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h),pygame.FULLSCREEN)
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()

# Dimensions des demi-tiles (64x64 => demi-dimension 32)
tile_width_half = 32
tile_height_half = 32

class Tile:
    """Classe représentant une tuile avec une image et des dimensions."""
    def __init__(self, image_path, width, height):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.width = width
        self.height = height
        self.width_half = width // 2
        self.height_half = height // 2

class TileMap:
    """Classe gérant la carte des tuiles."""
    def __init__(self, size, tile_grass, tile_wood, tile_gold, tile_test):
        self.size = size
        self.map_data = np.full((size, size), " ")  # Remplir la carte d'herbe
        self.tile_grass = tile_grass
        self.tile_wood = tile_wood
        self.tile_gold = tile_gold
        self.tile_test = tile_test
        self.add_wood_patches()
        self.add_gold_patches()
        self.add_special_block()

    def add_wood_patches(self):
        """Ajoute des paquets de bois (W) sur la carte."""
        num_patches = random.randint(10, 20)
        min_patch_size = 3
        max_patch_size = 7

        for _ in range(num_patches):
            patch_size = random.randint(min_patch_size, max_patch_size)
            start_x = random.randint(0, self.size - 1)
            start_y = random.randint(0, self.size - 1)

            wood_tiles = [(start_x, start_y)]
            self.map_data[start_y][start_x] = "W"  # Placer la première tuile de bois

            while len(wood_tiles) < patch_size:
                tile_x, tile_y = random.choice(wood_tiles)
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Choisir une direction
                new_x = tile_x + direction[0]
                new_y = tile_y + direction[1]

                if 0 <= new_x < self.size and 0 <= new_y < self.size:
                    if self.map_data[new_y][new_x] == " ":  # Placer du bois si la case est d'herbe
                        self.map_data[new_y][new_x] = "W"
                        wood_tiles.append((new_x, new_y))

    def add_gold_patches(self):
        """Ajoute des paquets d'or (G) sur la carte."""
        num_patches = random.randint(5, 10)  # Nombre de paquets d'or à générer
        min_patch_size = 2  # Taille minimale d'un paquet
        max_patch_size = 5  # Taille maximale d'un paquet

        for _ in range(num_patches):
            patch_size = random.randint(min_patch_size, max_patch_size)
            start_x = random.randint(0, self.size - 1)
            start_y = random.randint(0, self.size - 1)

            gold_tiles = [(start_x, start_y)]
            if self.map_data[start_y][start_x] == " ":
                self.map_data[start_y][start_x] = "G"  # Placer la première tuile d'or

            while len(gold_tiles) < patch_size:
                tile_x, tile_y = random.choice(gold_tiles)
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # (dx, dy)
                new_x = tile_x + direction[0]
                new_y = tile_y + direction[1]

                if 0 <= new_x < self.size and 0 <= new_y < self.size:
                    if self.map_data[new_y][new_x] == " ":
                        self.map_data[new_y][new_x] = "G"
                        gold_tiles.append((new_x, new_y))

    def render(self, display_surface, cam_x, cam_y):
        """Affiche la carte en fonction de la position de la caméra, centrée au milieu."""
        half_size = self.size // 2  # La moitié de la taille de la carte

        for row in range(self.size):
            for col in range(self.size):
                tile_type = self.map_data[row][col]
                if tile_type == " ":
                    tile = self.tile_grass
                    offset_y = 0
                elif tile_type == "W":
                    tile = self.tile_wood
                    offset_y = tile.height - self.tile_grass.height
                elif tile_type == "G":
                    tile = self.tile_gold
                    offset_y = tile.height - self.tile_grass.height
                elif tile_type == "T":  # Type de tuile pour un bloc spécial
                    tile = self.tile_test
                    offset_y = tile.height - self.tile_grass.height

                # Coordonnées cartésiennes centrées
                centered_col = col - half_size  # Décalage en X
                centered_row = row - half_size  # Décalage en Y

                # Conversion en coordonnées isométriques
                cart_x = centered_col * self.tile_grass.width_half
                cart_y = centered_row * self.tile_grass.height_half

                # Coordonnées isométriques avec prise en compte du décalage caméra
                iso_x = (cart_x - cart_y) - cam_x
                iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y

                # Affichage de la tuile
                display_surface.blit(tile.image, (iso_x, iso_y))

    def print_map(self):
        """Enregistre la carte dans un fichier texte."""
        with open('map_output.txt', 'w') as f:
            for row in self.map_data:
                f.write(" ".join(row) + "\n")

    def open_second_terminal(self):
        """Ouvre un nouveau terminal pour suivre l'affichage de la carte."""
        if os.name == 'posix':  # Si tu es sur un système Unix (Linux/MacOS)
            subprocess.Popen(['gnome-terminal', '--', 'tail', '-f', 'map_output.txt'])
        elif os.name == 'nt':  # Si tu es sur Windows
            subprocess.Popen(['start', 'cmd', '/K', 'type', 'map_output.txt'], shell=True)

    def add_special_block(self):
        """Ajoute un bloc spécial au centre de la carte."""
        center_x = self.size // 2
        center_y = self.size // 2

        print(center_x, center_y)
        self.map_data[center_y][center_x] = "T"  # Placer un bloc spécial au centre


class Game:
    """Classe principale gérant le jeu."""

    def __init__(self, screen_width, screen_height, map_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll_speed = 30

        # Charger les tuiles
        self.tile_grass = Tile('cube_grass.png', 64, 64)
        self.tile_wood = Tile('cube_grass - Copie.png', 128, 128)
        self.tile_gold = Tile('cube_rocky2.png', 64, 64)
        self.tile_test = Tile('cube_dirt.png', 64, 64)

        # Sélection de la carte
        self.map_size = map_size
        self.tile_map = None

        # Initialisation des coordonnées de la caméra
        self.cam_x, self.cam_y = self.center_camera_on_tile()

    def calculate_camera_limits(self):
        """Calcule les limites de la caméra pour empêcher le défilement hors de la carte."""
        # Taille de la moitié de la carte
        map_size_half = self.map_size // 2

        # Calcul des coins en coordonnées cartésiennes
        min_cart_x = -map_size_half * self.tile_grass.width_half
        max_cart_x = map_size_half * self.tile_grass.width_half
        min_cart_y = -map_size_half * self.tile_grass.height_half
        max_cart_y = map_size_half * self.tile_grass.height_half

        # Conversion des coins en isométriques
        min_iso_x = min_cart_x - max_cart_y
        max_iso_x = max_cart_x - min_cart_y
        min_iso_y = (min_cart_x + min_cart_y) // 2
        max_iso_y = (max_cart_x + max_cart_y) // 2

        # Ajustement pour la taille de l'écran
        min_cam_x = min_iso_x - (self.screen_width // 2) + screen_width // 2 + (-5 * self.tile_grass.width_half)
        max_cam_x = max_iso_x - (self.screen_width // 2) - screen_width // 2 + 5 * self.tile_grass.width_half
        min_cam_y = min_iso_y - (self.screen_height // 2) + screen_height // 2 + (-5 * self.tile_grass.width_half)
        max_cam_y = max_iso_y - (self.screen_height // 2) - screen_height // 2 + 5 * self.tile_grass.width_half

        return min_cam_x, min_cam_y, max_cam_x, max_cam_y

    def center_camera_on_tile(self):
        """Centre la caméra sur la tuile centrale de la carte."""
        center_x = self.map_size // 2
        center_y = self.map_size // 2

        # Conversion des coordonnées de la tuile centrale en isométriques
        tile_width_half = self.tile_grass.width_half
        tile_height_half = self.tile_grass.height_half
        cart_x = center_x * tile_width_half
        cart_y = center_y * tile_height_half
        iso_x = (cart_x - cart_y)
        iso_y = (cart_x - cart_y)//2
        print("iso_x:", iso_x)
        print ("iso_y:",iso_y)

        # Calculer la position de la caméra pour centrer cette tuile sur l'écran
        cam_x = (iso_x - self.screen_width // 2) + tile_width_half
        cam_y = -(iso_y + self.screen_height // 2 )

        print("-------------",cam_x, cam_y)
        return cam_x, cam_y
    
    
    #def start_game(self):
    #    if self.is_running:
    #        print("Le jeu '{self.name}' est déjà en route.")
    #    elif self.is_running == True: 
    #        print ("Le jeu '{self.name}' a commencé.")
    #def pause_game(self):
    #    if self.is_running:
    #        self.is_running = False
    #        print ("Le jeu '{self.name}' est en pause.")
    #    else: 
    #        print ("Le jeu '{self.name}' est déjà en pause.")
    #def end_game(self):
    #    if self.is_running:
    #        self.is_running = False
    #    print("Le jeu '{self.name}' est terminé. Vous avez joué {self.game_time} minutes.")

        # Définir les couleurs
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)

        # Police et surface
        font = pygame.font.Font(None, 74)
        small_font = pygame.font.Font(None, 36)
        DISPLAYSURF.fill(BLACK)

        # Texte du menu
        menu_text = font.render("Choisissez une carte:", True, WHITE)
        DISPLAYSURF.blit(menu_text, (100, 100))

        # Options de cartes
        card1_text = small_font.render("Lean", True, WHITE)
        card2_text = small_font.render("Mean", True, WHITE)
        card3_text = small_font.render("Marines", True, WHITE)
        load_data_text = small_font.render("4. Charger la partie sauvegarder", True, GREEN)

        # Positions des textes
        card1_rect = card1_text.get_rect(topleft=(150, 200))
        card2_rect = card2_text.get_rect(topleft=(150, 250))
        card3_rect = card3_text.get_rect(topleft=(150, 300))
        load_data_rect = load_data_text.get_rect(topleft=(150, 400))

        DISPLAYSURF.blit(card1_text, (150, 200))
        DISPLAYSURF.blit(card2_text, (150, 250))
        DISPLAYSURF.blit(card3_text, (150, 300))
        DISPLAYSURF.blit(load_data_text, (150, 400))

        pygame.display.update()

        return card1_rect, card2_rect, card3_rect, load_data_rect

    def load_data(self, path):
        try:
            with open(path, 'r') as fichier:
                print(f"Données chargées depuis {path}")
                data = json.load(fichier)  # Charger le contenu JSON
                print(f"Données lues : {data}")  # Affiche les données lues
                return data
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
        return None

    def handle_camera_movement(self, keys):
        """Gère le mouvement de la caméra avec des limites."""
        min_cam_x, min_cam_y, max_cam_x, max_cam_y = self.calculate_camera_limits()

        if keys[K_q]:
            self.cam_x = max(self.cam_x - self.scroll_speed, min_cam_x)
        if keys[K_d]:
            self.cam_x = min(self.cam_x + self.scroll_speed, max_cam_x)
        if keys[K_z]:
            self.cam_y = max(self.cam_y - self.scroll_speed, min_cam_y)
        if keys[K_s]:
            self.cam_y = min(self.cam_y + self.scroll_speed, max_cam_y)

    def run(self):
        """Boucle principale du jeu."""
        running = True
        menu = True
        load = False

        while running:
            for event in pygame.event.get():
                if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if menu:
                    card1_rect, card2_rect, card3_rect, load_data_rect = self.show_menu()

                    if event.type == KEYDOWN :
                        if event.key == K_1:
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold, self.tile_test)
                            self.tile_map.open_second_terminal()
                            menu = False
                        elif event.key == pygame.K_2:
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold, self.tile_test)
                            # self.tile_map.open_second_terminal()
                            menu = False
                        elif event.key == pygame.K_3:
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold, self.tile_test)
                            # self.tile_map.open_second_terminal()
                            menu = False
                        elif event.key == pygame.K_4:
                            print("Chargement des données sauvegardées")
                            # Charger les données sauvegardées
                            menu = False
                            load = True

                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        # Obtenir la position de la souris
                        mouse_pos = pygame.mouse.get_pos()

                        # Vérifier si la souris est sur une option de menu
                        if card1_rect.collidepoint(mouse_pos):
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold, self.tile_test)
                            self.tile_map.open_second_terminal()
                            menu = False
                        elif card2_rect.collidepoint(mouse_pos):
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold, self.tile_test)
                            self.tile_map.open_second_terminal()
                            menu = False
                        elif card3_rect.collidepoint(mouse_pos):
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold, self.tile_test)
                            self.tile_map.open_second_terminal()
                            menu = False
                        elif load_data_rect.collidepoint(mouse_pos):
                            print("Chargement des données sauvegardées")
                            menu = False
                            load = True

            if load:
                save = self.load_data("save.json")
                if save:  # Assure-toi que save n'est pas None
                    print(f"Données chargées : {save['taille']}")
                    self.tile_map = TileMap(save['taille'], self.tile_grass, self.tile_wood, self.tile_gold, self.tile_test)
                    self.tile_map.open_second_terminal()
                    # Traiter les données chargées
                    load = False
                else:
                    print("Aucune donnée n'a été chargée.")
            elif not menu:
                keys = pygame.key.get_pressed()
                self.handle_camera_movement(keys)

                DISPLAYSURF.fill((0, 0, 0))  # Effacer l'écran
                self.tile_map.print_map()
                self.tile_map.render(DISPLAYSURF, self.cam_x, self.cam_y)

            pygame.display.update()
            FPSCLOCK.tick(60)


# Initialisation et lancement du jeu
game = Game(screen_width, screen_height, map_size = 120)
game.run()
