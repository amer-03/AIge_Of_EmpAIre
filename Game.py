import pygame
from pygame.locals import *
<<<<<<< Updated upstream
import sys
from math import *
import json
from Map import *
=======
from Minimap import Minimap
import Units
from constants import *
from TileMap import TileMap
from Barre_ressource import Barre_ressources
from Units import Unit
from Buildings import Buildings
import curses
import keyboard
import time
import threading
>>>>>>> Stashed changes

class Game:
    """Classe principale gérant le jeu."""

    def __init__(self, screen_width, screen_height, map_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll_speed = 30

        # Charger les tuiles
        self.tile_grass = Tile('Image/grass2.png', 64, 64)
        self.tile_wood = Tile('Image/tree.png', 128, 128)
        self.tile_gold = Tile('Image/gold2.png', 128, 128)

        # Sélection de la carte
        self.map_size = map_size
        self.tile_map = None

        # Initialisation des coordonnées de la caméra
        self.cam_x, self.cam_y = self.center_camera_on_tile()

<<<<<<< Updated upstream
=======
        # MINIMAP
        self.mini_map_size_x = 490  # Largeur de la mini-carte
        self.mini_map_size_y = 270  # Hauteur de la mini-carte  # Taille carrée de la mini-carte
        self.mini_map_scale = 4  # Échelle de réduction de la mini-carte
        self.cam_mini_x, self.cam_mini_y = self.center_camera_on_tile()

        # BARRE JOUEURS
        self.barre_ressources = Barre_ressources
        self.barres = [
            Barre_ressources("images/bois_barre.png", "w", 24),
            Barre_ressources("images/or_barre.png", "g", 24),
            Barre_ressources("images/food_barre.png", "f", 24),
            Barre_ressources("images/entite.png", "U", 24)
        ]

        self.barre_units = [
            Barre_ressources("images/villageois.webp", "v", 24),
            Barre_ressources("images/epeiste.png", "s", 24),
            Barre_ressources("images/cavalier.png", "h", 24),
            Barre_ressources("images/archer.png", "a", 24)
        ]

        self.barre_builds = [
            Barre_ressources("images/Town_Center.webp", "T", 24),
            Barre_ressources("images/House.webp", "H", 24),
            Barre_ressources("images/Camp.png", "C", 24),
            Barre_ressources("images/Farm - Copie.png", "F", 24),
            Barre_ressources("images/Barracks.png", "B", 24),
            Barre_ressources("images/Stable.png", "S", 24),
            Barre_ressources("images/Archery Range.png", "A", 24),
            Barre_ressources("images/Keep.png", "K", 24)
        ]

        self.f1_active = False
        self.f2_active = False
        self.f3_active = False

        # MENU DEPART

        self.selected_option = None
        self.menu_active = True
        self.selected_unit = None
        self.selected_map = None
        self.joueur = 0
        self.compteur = compteurs_joueurs
        self.n = 2  # Définition du nombre de joueurs
        self.dropdown_open = False  # Indicateur pour savoir si la liste déroulante est ouverte
        self.dropdown_rect = pygame.Rect(screen_width // 2 - 50, 400, 100, 30)  # Rect du bouton de la liste déroulante
        self.options_rects = []

        # TERMINAL
        self.terminal_x = 0
        self.terminal_y = 0
        self.terminal_active = False
        self.position_initiale = (size // 2, size // 2)  # Position initiale du joueur

        # UNITS
        # self.swordsman = Units.Swordsman()
        self.unit = Unit()

        # BUILDS
        self.buildings = Buildings()

        self.minimap = Minimap()
        self.camera_pos = [0, 0]
        self.viewport_size = (800, 600)  # Adjust to your screen size

        # Initialize map_data from tile_map
        self.map_data = [[' ' for _ in range(size)] for _ in range(size)]  # size should be defined
        self.update_map_data()  # New method to sync tile_map with map_data

>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
            self.cam_y = min(self.cam_y + self.scroll_speed, max_cam_y)
=======
            self.cam_y = min(self.cam_y + speed, max_cam_y)  # Déplace vers le bas

    def handle_mini_map_click(self, mouse_pos):
        # Create minimap rectangle
        mini_map_rect = pygame.Rect(
            DISPLAYSURF.get_width() - self.mini_map_size_x - 10,
            DISPLAYSURF.get_height() - self.mini_map_size_y - 10,
            self.mini_map_size_x,
            self.mini_map_size_y
        )

        if mini_map_rect.collidepoint(mouse_pos):
            # Calculate coordinates in minimap
            mini_map_x = mouse_pos[0] - (DISPLAYSURF.get_width() - self.mini_map_size_x - 10)
            mini_map_y = mouse_pos[1] - (DISPLAYSURF.get_height() - self.mini_map_size_y - 10)

            # Convert to world coordinates
            scale_x = size * (tile_grass.width_half * 2) / self.mini_map_size_x
            scale_y = size * tile_grass.height_half / self.mini_map_size_y

            world_x = int((mini_map_x - self.mini_map_size_x // 2) * scale_x)
            world_y = int((mini_map_y - self.mini_map_size_y // 2) * scale_y)

            # Update both camera positions
            self.cam_x = world_x - DISPLAYSURF.get_width() // 2
            self.cam_y = world_y - DISPLAYSURF.get_height() // 2
            self.camera_pos = [self.cam_x, self.cam_y]

    def create_count(self):
        for i in range(1, self.n + 1):
            # Crée un dictionnaire de compteurs pour chaque joueur
            compteurs_joueurs[f'joueur_{i}'] = {
                # Ressources
                'ressources': {
                    'w': 0,  # Bois
                    'f': 0,  # Nourriture
                    'g': 0,  # Or
                    'U': 0  # Unités générales (ou autre ressource spéciale)
                },
                # Unités
                'unites': {
                    'v': 0,  # Villageois
                    's': 0,  # Swordsman (épéiste)
                    'h': 0,  # Horseman (cavalier)
                    'a': 0  # Archer
                },
                # Bâtiments
                'batiments': {
                    'T': 0,  # Tour de guet
                    'H': 0,  # Maison
                    'C': 0,  # Centre-ville
                    'F': 0,  # Ferme
                    'B': 0,  # Caserne
                    'S': 0,  # Forge
                    'A': 0,  # Académie
                    'K': 0  # Château
                }
            }

    def initialize_resources(self, unit):
        self.create_count()
        # Parcourt chaque joueur dans le dictionnaire pour initialiser les ressources
        for joueur, compteurs in compteurs_joueurs.items():
            if unit == "Lean":
                compteurs['ressources']['w'] = 200
                compteurs['ressources']['f'] = 50
                compteurs['ressources']['g'] = 50
                compteurs['unites']['v'] = 1
                compteurs['unites']['a'] = 1
                if isinstance(compteurs['unites'], dict):
                    compteurs['ressources']['U'] = sum(compteurs['unites'].values())
                compteurs['batiments']['T'] = 2
                compteurs['batiments']['B'] = 2
                compteurs['batiments']['S'] = 2
                compteurs['batiments']['K'] = 2
                compteurs['batiments']['H'] = 2

            elif unit == "Mean":
                compteurs['ressources']['w'] = 2000
                compteurs['ressources']['f'] = 2000
                compteurs['ressources']['g'] = 2000
                compteurs['unites']['v'] = 3
                compteurs['unites']['a'] = 3
                if isinstance(compteurs['unites'], dict):
                    compteurs['ressources']['U'] = sum(compteurs['unites'].values())
                compteurs['batiments']['T'] = 1
            elif unit == "Marines":
                compteurs['ressources']['w'] = 20000
                compteurs['ressources']['f'] = 20000
                compteurs['ressources']['g'] = 20000
                compteurs['unites']['v'] = 15
                if isinstance(compteurs['unites'], dict):
                    compteurs['ressources']['U'] = sum(compteurs['unites'].values())
                compteurs['batiments']['T'] = 3
                compteurs['batiments']['B'] = 2
                compteurs['batiments']['S'] = 2
                compteurs['batiments']['A'] = 2

    def draw_resources(self):
        x_barre_base = 100  # Position de départ en X pour la première colonne
        y_barre_base = 40  # Position de départ en Y pour la première ligne

        espacement_horizontal = barre_width + 200  # Espacement entre les colonnes
        espacement_vertical = 200  # Espacement entre les lignes

        total_images = len(self.barres)
        total_images_barre_builds = len(self.barre_builds)

        for index, (joueur, compteurs) in enumerate(compteurs_joueurs.items()):
            # Calcul de la position en X et Y pour chaque joueur
            colonne = index % 2  # 0 pour la première colonne, 1 pour la seconde
            ligne = index // 2  # Numéro de la ligne

            x_barre = x_barre_base + colonne * espacement_horizontal
            y_barre = y_barre_base + ligne * espacement_vertical

            # print (x_barre, y_barre)

            # Affiche les ressources (f1_active)
            if self.f1_active:
                self.barres[0].barre(DISPLAYSURF, x_barre, y_barre)
                for i, barre in enumerate(self.barres):
                    type = ["w", "g", "f", "U"][i]
                    barre.draw(DISPLAYSURF, x_barre, y_barre, self.compteur[joueur]['ressources'][type], i,
                               total_images)

            # Affiche les unités (f2_active)
            if self.f2_active:
                for barre_unit in self.barres:
                    barre_unit.barre_units(DISPLAYSURF, x_barre, y_barre + barre_height)
                for i, barre in enumerate(self.barre_units):
                    type = ["v", "s", "h", "a"][i]
                    barre.draw_barre_units(DISPLAYSURF, x_barre, y_barre + barre_height,
                                           self.compteur[joueur]['unites'][type], i, total_images)

            # Affiche les constructions (f3_active)
            if self.f3_active:
                for barre_builds in self.barres:
                    barre_builds.barre_builds(DISPLAYSURF, x_barre, y_barre + barre_height + barre_units_height)
                for i, barre in enumerate(self.barre_builds):
                    type = ["T", "H", "C", "F", "B", "S", "A", "K"][i]
                    barre.draw_barre_units(DISPLAYSURF, x_barre, y_barre + barre_height + barre_units_height,
                                           self.compteur[joueur]['batiments'][type], i, total_images_barre_builds)

    def draw_map_in_terminal(self, stdscr):
        stdscr.clear()
        stdscr.nodelay(1)
        stdscr.timeout(500)
        stdscr.addstr(0, 0, "Démarrage de l'affichage...")  # Message de démarrage

        # Dimensions du terminal
        max_rows, max_cols = stdscr.getmaxyx()

        map_rows = size
        map_cols = size

        while self.terminal_active:
            stdscr.clear()

            # Met à jour la position du joueur
            player_x, player_y = self.tile_map.position_initiale

            # Ajuster le viewport pour centrer sur le joueur
            view_top = max(0, min(player_x - max_rows // 2, map_rows - max_rows))
            view_left = max(0, min(player_y - max_cols // 2, map_cols - max_cols))

            # Affiche la partie visible de la carte
            for row in range(view_top, min(view_top + max_rows, map_rows)):
                row_str = ""
                for col in range(view_left, min(view_left + max_cols, map_cols)):
                    if (row, col) == (player_x, player_y):
                        row_str += "P"  # Affiche le joueur
                    else:
                        row_str += map_data[row][col]

                # Limiter l'affichage au nombre de colonnes disponibles
                try:
                    if row - view_top < max_rows:
                        stdscr.addstr(row - view_top, 0, row_str[:max_cols])
                except curses.error:
                    # Ignore les erreurs d'affichage hors limites
                    pass

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

            time.sleep(0.1)  # Pause pour éviter d'utiliser trop de CPU

    def ouvrir_terminal(self):
        if self.terminal_active:
            # Ferme le terminal
            self.terminal_active = False
            # print("avant",self.cam_x, self.cam_y)

            # Récupération de la position du joueur
            y, x = self.tile_map.position_initiale  # Assurez-vous de l'ordre ici (col, row)
            half_size = size // 2  # Assurez-vous que la taille de la carte est correctement définie

            # Décalage centré pour le joueur
            centered_col = y - half_size
            centered_row = x - half_size

            # Conversion en coordonnées isométriques
            cart_x = centered_row * tile_grass.width_half
            cart_y = centered_col * tile_grass.width_half

            iso_x = cart_x - cart_y  # Ne pas soustraire cam_x ici
            iso_y = (cart_x + cart_y) / 2  # Ne pas soustraire cam_y ici

            self.cam_x = iso_x - (screen_width // 2) + tile_grass.width_half
            self.cam_y = iso_y - (screen_height // 2)

            print("Caméra après ajustement:", self.cam_x, self.cam_y)

        else:

            iso_x = self.cam_x + (screen_width // 2) - tile_grass.width_half
            iso_y = self.cam_y + (screen_height // 2)

            # Conversion des coordonnées isométriques en coordonnées cartésiennes
            cart_x = (iso_x + 2 * iso_y) / 2
            cart_y = (2 * iso_y - iso_x) / 2  # Formule inverse pour obtenir cart_y

            half_size = len(self.tile_map.get_map_data()) // 2  # Taille centrée de la carte

            centered_col = int(cart_y / tile_grass.height_half)  # Indice de la colonne
            centered_row = int(cart_x / tile_grass.width_half)  # Indice de la ligne

            # Récupération des coordonnées de la matrice
            y = centered_row + half_size  # Ajustement en fonction de half_size
            x = centered_col + half_size  # Ajustement en fonction de half_size

            self.tile_map.position_initiale = x, y
            # Ouvre le terminal dans un nouveau thread
            self.terminal_active = True
            terminal_thread = threading.Thread(target=curses.wrapper, args=(self.draw_map_in_terminal,))
            terminal_thread.daemon = True
            terminal_thread.start()



>>>>>>> Stashed changes

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
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold)
                            self.tile_map.open_second_terminal()
                            menu = False
                        elif event.key == pygame.K_2:
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold)
                            # self.tile_map.open_second_terminal()
                            menu = False
                        elif event.key == pygame.K_3:
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold)
                            # self.tile_map.open_second_terminal()
                            menu = False
                        elif event.key == pygame.K_4:
                            print("Chargement des données sauvegardées")
                            # Charger les données sauvegardées
                            menu = False
                            load = True
                        elif event.type == KEYDOWN:
                            if event.key == K_EQUALS:  # Touche + pour zoom in
                                self.tile_map = min(self.tile_map + 0.1, 3.0)  # Limite à un zoom maximum de 3x
                        elif event.key == K_MINUS:  # Touche - pour zoom out
                            self.tile_map = max(self.tile_map - 0.1, 0.5)  # Limite à un zoom minimum de 0.5x

        # Zoom avec la molette de la souris
                        elif event.type == MOUSEBUTTONDOWN:
                            if event.button == 4:  # Molette vers le haut (zoom in)
                                self.tile_map = min(self.tile_map + 0.1, 3.0)
                        elif event.button == 5:  # Molette vers le bas (zoom out)
                            self.tile_map = max(self.tile_map - 0.1, 0.5)

                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        # Obtenir la position de la souris
                        mouse_pos = pygame.mouse.get_pos()

                        # Vérifier si la souris est sur une option de menu
                        if card1_rect.collidepoint(mouse_pos):
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold)
                            self.tile_map.open_second_terminal()
                            menu = False
                        elif card2_rect.collidepoint(mouse_pos):
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold)
                            self.tile_map.open_second_terminal()
                            menu = False
                        elif card3_rect.collidepoint(mouse_pos):
                            self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold)
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
                    self.tile_map = TileMap(save['taille'], self.tile_grass, self.tile_wood, self.tile_gold)
                    self.tile_map.open_second_terminal()
                    # Traiter les données chargées
                    load = False
                else:
                    print("Aucune donnée n'a été chargée.")
            elif not menu:
                keys = pygame.key.get_pressed()
                self.handle_camera_movement(keys)

<<<<<<< Updated upstream
                DISPLAYSURF.fill((0, 0, 0))  # Effacer l'écran
                self.tile_map.print_map()
                self.tile_map.render(DISPLAYSURF, self.cam_x, self.cam_y)
=======
                self.draw_resources()

                self.buildings.affichage()
                pygame.display.update()
                pygame.display.flip()
                #self.unit.initialiser_unit_list()
                #print(tuiles)

            self.update_map_data()  # Update map_data before minimap update
            self.minimap.update(self.map_data, self.camera_pos, self.viewport_size)
>>>>>>> Stashed changes

            self.draw_minimap_viewport()
            pygame.display.update()
            FPSCLOCK.tick(60)

<<<<<<< Updated upstream

# Initialisation et lancement du jeu
game = Game(screen_width, screen_height, map_size = 120)
game.run()
=======
    def update_map_data(self):
        """Sync tile_map data to map_data for minimap"""
        # Assuming TileMap stores its data in self.tiles or similar
        tiles = self.tile_map.tiles if hasattr(self.tile_map, 'tiles') else []
        
        # Clear map_data
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[y])):
                self.map_data[y][x] = ' '
        
        # Update from buildings
        if hasattr(self.buildings, 'tuiles'):
            for pos, tuile in self.buildings.tuiles.items():
                x, y = pos
                if 0 <= x < len(self.map_data) and 0 <= y < len(self.map_data[0]):
                    if 'batiments' in tuile:
                        for joueur in tuile['batiments']:
                            for batiment in tuile['batiments'][joueur]:
                                self.map_data[y][x] = batiment[0].upper()
        
        # Update from resources if they exist
        if hasattr(self.tile_map, 'resources'):
            for pos, resource in self.tile_map.resources.items():
                x, y = pos
                if 0 <= x < len(self.map_data) and 0 <= y < len(self.map_data[0]):
                    self.map_data[y][x] = resource[0].upper()

    def draw_minimap_viewport(self):
        # Calculate viewport rectangle in minimap coordinates
        viewport_x = (self.cam_x + DISPLAYSURF.get_width() // 2) * self.mini_map_size_x / (size * tile_grass.width_half * 2)
        viewport_y = (self.cam_y + DISPLAYSURF.get_height() // 2) * self.mini_map_size_y / (size * tile_grass.height_half * 2)
        
        # Calculate viewport size in minimap scale
        viewport_w = DISPLAYSURF.get_width() * self.mini_map_size_x / (size * tile_grass.width_half * 2)
        viewport_h = DISPLAYSURF.get_height() * self.mini_map_size_y / (size * tile_grass.height_half * 2)
        
        # Draw white rectangle on minimap
        pygame.draw.rect(
            DISPLAYSURF,
            (255, 255, 255),  # White color
            (
                DISPLAYSURF.get_width() - self.mini_map_size_x - 10 + viewport_x,
                DISPLAYSURF.get_height() - self.mini_map_size_y - 10 + viewport_y,
                viewport_w,
                viewport_h
            ),
            1  # Rectangle border thickness
        )
>>>>>>> Stashed changes
