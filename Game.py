import pygame
from pygame.locals import *
import sys
from math import *
import json
from Map import *


class Game:
    """Classe principale gérant le jeu."""

    def __init__(self, screen_width, screen_height, map_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll_speed = 30

        # Charger les tuiles
        self.tile_grass = Tile('Image/grass2.png', 64, 64)
        self.tile_wood = Tile('Image/tree.png', 128, 128)
        self.tile_gold = Tile('Image/cube_rocky2.png', 64, 64)
        self.tile_test = Tile('Image/cube_dirt.png', 64, 64)

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

    def show_menu(self):
        """Affiche un menu pour choisir la carte et charger les données sauvegardées."""
        pygame.init()

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
