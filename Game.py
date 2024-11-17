import pygame
import sys
import json
from pygame.locals import *

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

class Game:
    """Classe principale gérant le jeu."""

    def __init__(self):

        #MAP
        self.scroll_speed = 30
        self.tile_map = None
        self.tile_map = TileMap()
        self.cam_x, self.cam_y = self.center_camera_on_tile()

        #MINIMAP
        self.mini_map_size_x = 490  # Largeur de la mini-carte
        self.mini_map_size_y = 270  # Hauteur de la mini-carte  # Taille carrée de la mini-carte
        self.mini_map_scale = 4 # Échelle de réduction de la mini-carte
        self.cam_mini_x, self.cam_mini_y = self.center_camera_on_tile()

        #BARRE JOUEURS
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

        #MENU DEPART

        self.selected_option = None
        self.menu_active = True
        self.selected_unit=None
        self.selected_map=None
        self.joueur = 0
        self.compteur = compteurs_joueurs
        self.n = 2  # Définition du nombre de joueurs
        self.dropdown_open = False  # Indicateur pour savoir si la liste déroulante est ouverte
        self.dropdown_rect = pygame.Rect(screen_width // 2 - 50, 400, 100, 30)  # Rect du bouton de la liste déroulante
        self.options_rects = []



        #TERMINAL
        self.terminal_x = 0
        self.terminal_y = 0
        self.terminal_active = False
        self.position_initiale = (size // 2, size // 2)  # Position initiale du joueur


        #UNITS
        #self.swordsman = Units.Swordsman()
        self.unit = Unit()

        #BUILDS
        self.buildings = Buildings()



    def calculate_camera_limits(self):
        """Calcule les limites de la caméra pour empêcher le défilement hors de la carte."""
        # Taille de la moitié de la carte
        map_size_half = size // 2

        # Calcul des coins en coordonnées cartésiennes
        min_cart_x = -map_size_half * tile_grass.width_half
        max_cart_x = map_size_half * tile_grass.width_half
        min_cart_y = -map_size_half * tile_grass.height_half
        max_cart_y = map_size_half * tile_grass.height_half

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

    def center_camera_on_tile(self):
        """Centre la caméra sur la tuile centrale de la carte."""
        center_x = size // 2
        center_y = size // 2

        # Conversion des coordonnées de la tuile centrale en isométriques
        tile_width_half = tile_grass.width_half
        tile_height_half = tile_grass.height_half
        cart_x = center_x * tile_width_half
        cart_y = center_y * tile_height_half
        iso_x = (cart_x - cart_y)
        iso_y = (cart_x - cart_y)//2

        cam_x = (iso_x - screen_width // 2) + tile_width_half
        cam_y = -(iso_y + screen_height // 2 )

        return cam_x, cam_y

    def show_menu(self):
        """Affiche un menu pour choisir la carte et charger les données sauvegardées."""
        font = pygame.font.Font(None, 74)
        small_font = pygame.font.Font(None, 36)

        fond_image = pygame.image.load('images/test4.jpg')
        fond_image = pygame.transform.scale(fond_image, (screen_width, screen_height))
        DISPLAYSURF.blit(fond_image, (0, 0))

        menu_text = font.render("Menu Principal", True, BLACK)
        menu_text_rect = menu_text.get_rect(center=(screen_width // 2, 100))
        DISPLAYSURF.blit(menu_text, menu_text_rect)

        card_color1 = YELLOW if self.selected_unit == "Lean" else BLACK
        card_color2 = YELLOW if self.selected_unit == "Mean" else BLACK
        card_color3 = YELLOW if self.selected_unit == "Marines" else BLACK
        card_color4 = YELLOW if self.selected_map == "Map 1" else BLACK
        card_color5 = YELLOW if self.selected_map == "Map 2" else BLACK

        card1_text = small_font.render("Lean", True, card_color1)
        card2_text = small_font.render("Mean", True, card_color2)
        card3_text = small_font.render("Marines", True, card_color3)
        card4_text = small_font.render("Map 1", True, card_color4)
        card5_text = small_font.render("Map 2", True, card_color5)
        start_text = small_font.render("Commencer la Partie", True, GREEN)

        self.card1_rect = card1_text.get_rect(topleft=(screen_width //2 - 150, 200))
        self.card2_rect = card2_text.get_rect(topleft=(screen_width //2 - 150, 250))
        self.card3_rect = card3_text.get_rect(topleft=(screen_width //2 - 150, 300))
        self.card4_rect = card4_text.get_rect(topleft=(screen_width //2 + 50, 200))
        self.card5_rect = card5_text.get_rect(topleft=(screen_width //2 + 50, 250))
        self.start_rect = start_text.get_rect(center=(screen_width // 2 , 500))

        DISPLAYSURF.blit(card1_text, self.card1_rect.topleft)
        DISPLAYSURF.blit(card2_text, self.card2_rect.topleft)
        DISPLAYSURF.blit(card3_text, self.card3_rect.topleft)
        DISPLAYSURF.blit(card4_text, self.card4_rect.topleft)
        DISPLAYSURF.blit(card5_text, self.card5_rect.topleft)
        DISPLAYSURF.blit(start_text, self.start_rect.topleft)

        mini_texte = pygame.font.Font(None, 24)
        # Affiche le bouton de la liste déroulante
        dropdown_text = mini_texte.render(f"{self.n} joueurs", True, BLACK)
        pygame.draw.rect(DISPLAYSURF, GRAY, self.dropdown_rect)
        DISPLAYSURF.blit(dropdown_text, (self.dropdown_rect.x + 10, self.dropdown_rect.y + 5))

        # Si la liste déroulante est ouverte, afficher les options de 2 à 10
        if self.dropdown_open:
            for i in range(2, 11):
                option_rect = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + (i - 1) * 30 + 30, 100, 30)
                self.options_rects.append(option_rect)
                pygame.draw.rect(DISPLAYSURF, WHITE, option_rect)
                option_text = mini_texte.render(f"{i} joueurs", True, BLACK)
                DISPLAYSURF.blit(option_text, (option_rect.x + 10, option_rect.y + 5))

        pygame.display.update()


    def handle_menu_events(self, event):
        """Gère les événements liés au menu principal."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Vérifier la sélection des unités
            x, y = event.pos

            if self.dropdown_rect.collidepoint(x, y):
                self.dropdown_open = not self.dropdown_open  # Ouvrir ou fermer la liste déroulante

            # Si la liste déroulante est ouverte, vérifier si clic sur une option
            elif self.dropdown_open:
                for i, option_rect in enumerate(self.options_rects, start=2):
                    if option_rect.collidepoint(x, y):
                        self.n = i  # Met à jour le nombre de joueurs
                        self.dropdown_open = False  # Ferme la liste déroulante
                        self.options_rects = []  # Réinitialise les rectangles des options
                        break  # Sortir de la boucle pour éviter les vérifications inutiles


            # Si clic en dehors de la liste déroulante, fermer la liste
            else:
                self.dropdown_open = False

            if self.card1_rect.collidepoint(event.pos):
                self.selected_unit = "Lean"
                self.initialize_resources(self.selected_unit)
            elif self.card2_rect.collidepoint(event.pos):
                self.selected_unit = "Mean"
                self.initialize_resources(self.selected_unit)
            elif self.card3_rect.collidepoint(event.pos):
                self.selected_unit = "Marines"
                self.initialize_resources(self.selected_unit)

            elif self.card4_rect.collidepoint(event.pos):
                self.selected_map = "Map 1"
            elif self.card5_rect.collidepoint(event.pos):
                self.selected_map = "Map 2"

            elif self.start_rect.collidepoint(event.pos) and self.selected_unit and self.selected_map:
                if self.selected_map == 'Map 1':
                    self.tile_map.mode("patches")
                else:
                    self.tile_map.mode("middle")
                # Fermer le menu
                self.menu_active = False
                self.tile_map.render(DISPLAYSURF, self.cam_x, self.cam_y)
                position = self.unit.placer_joueurs_cercle(self.n, 50, map_size // 2, map_size // 2)
                print (position)

                self.initialize_resources(self.selected_unit)
                self.buildings.initialisation_compteur(position)
                self.unit.initialisation_compteur(position)

                # Si clic sur le bouton de la liste déroulante





    def display_option(self, text, x, y, is_selected):
        """Affiche une option avec un style visuel pour la sélection."""
        color = (0, 255, 0) if is_selected else (255, 255, 255)
        option_text = self.small_font.render(text, True, color)
        option_rect = option_text.get_rect(topleft=(x, y))
        DISPLAYSURF.blit(option_text, option_rect)
        return option_rect

    def load_game_data(self):
        """Charge les données sauvegardées, si disponible."""
        save_data = self.load_data("save.json")
        if save_data:
            print(f"Données chargées : {save_data['taille']}")

            self.load_active = False
        else:
            print("Aucune donnée n'a été chargée.")
            self.menu_active = True  # Revenir au menu si le chargement échoue

    def draw_mini_map(self, display_surface):
        """Affiche une version réduite de la carte en bas à gauche, orientée de manière isométrique."""
        losange_surface = pygame.Surface((self.mini_map_size_x, self.mini_map_size_y), pygame.SRCALPHA)
        losange_surface.fill((0, 0, 0, 0))  # Remplir de transparent

        mini_map_surface = pygame.Surface((self.mini_map_size_x, self.mini_map_size_y), pygame.SRCALPHA)
        mini_map_surface.fill((0, 0, 0, 0))  # Fond transparent
        tile_width_half = 1
        tile_height_half = 1

        for row in range(size):
            for col in range(size):
                tile_type = map_data[row][col]

                # Couleur des tuiles sur la mini-carte
                if tile_type == " ":
                    color = (34, 139, 34)  # Vert pour l'herbe
                elif tile_type == "W":
                    color = (139, 69, 19)  # Marron pour le bois
                elif tile_type == "G":
                    color = (255, 215, 0)  # Jaune pour l'or
                elif tile_type == "T":
                    color = (128, 128, 128)  # Gris pour le bloc spécial

                centered_col = col - (size // 2)
                centered_row = row - (size // 2)

                cart_x = centered_col * tile_width_half * self.mini_map_scale
                cart_y = centered_row * tile_height_half * self.mini_map_scale

                iso_x = (cart_x - cart_y) / 2 + self.mini_map_size_x // 2
                iso_y = (cart_x + cart_y) / 4 + self.mini_map_size_y // 2

                # Dessin de la tuile sur la mini-carte
                pygame.draw.rect(mini_map_surface, color, (iso_x, iso_y, self.mini_map_scale, self.mini_map_scale))

        losange_points = [
            (self.mini_map_size_x // 2+2, 12),  # Point supérieur
            (self.mini_map_size_x +1, self.mini_map_size_y // 2 ),  # Point droit
            (self.mini_map_size_x // 2+2, self.mini_map_size_y-12),  # Point inférieur
            (2, self.mini_map_size_y // 2)  # Point gauche
        ]

        pygame.draw.polygon(losange_surface, (0, 0, 0), losange_points, 2)  # Contour noir de 2 pixels
        losange_surface.blit(mini_map_surface, (0, 0))  # Positionner la mini-carte sur le losange

        # Afficher le losange sur l'écran principal
        display_surface.blit(losange_surface, (
            screen_width - self.mini_map_size_x - 10, screen_height - self.mini_map_size_y - 10))

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

    def handle_mini_map_click(self, mouse_pos):
        """Gère le clic sur la mini-carte et déplace la caméra."""
        # Définir la zone de la mini-carte
        mini_map_rect = pygame.Rect(screen_width - self.mini_map_size_x - 10,
                                    screen_height - self.mini_map_size_y - 10,
                                    self.mini_map_size_x, self.mini_map_size_y)

        if mini_map_rect.collidepoint(mouse_pos):
            # Calculer les coordonnées dans la mini-carte
            mini_map_x = mouse_pos[0] - (screen_width - self.mini_map_size_x - 10)
            mini_map_y = mouse_pos[1] - (screen_height - self.mini_map_size_y - 10)

            scale_x = size * (tile_grass.width_half*2) / self.mini_map_size_x
            scale_y = size * tile_grass.height_half / self.mini_map_size_y

            world_x = int((mini_map_x - self.mini_map_size_x //2) * scale_x)
            world_y = int((mini_map_y - self.mini_map_size_y // 2) * scale_y)

            self.cam_x = world_x - screen_width // 2
            self.cam_y = world_y - screen_height // 2

    def create_count(self):
        for i in range(1, self.n + 1):
            # Crée un dictionnaire de compteurs pour chaque joueur
            compteurs_joueurs[f'joueur_{i}'] = {
                 # Ressources
                'ressources': {
                    'w': 0,  # Bois
                    'f': 0,  # Nourriture
                    'g': 0,  # Or
                    'U': 0   # Unités générales (ou autre ressource spéciale)
                },
                # Unités
                'unites': {
                    'v': 0,  # Villageois
                    's': 0,  # Swordsman (épéiste)
                    'h': 0,  # Horseman (cavalier)
                    'a': 0   # Archer
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
                    'K': 0   # Château
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
                compteurs['unites']['v'] = 3
                compteurs['batiments']['T'] = 1
            elif unit == "Mean":
                compteurs['ressources']['w'] = 2000
                compteurs['ressources']['f'] = 2000
                compteurs['ressources']['g'] = 2000
                compteurs['unites']['v'] = 3
                compteurs['batiments']['T'] = 1
            elif unit == "Marines":
                compteurs['ressources']['w'] = 20000
                compteurs['ressources']['f'] = 20000
                compteurs['ressources']['g'] = 20000
                compteurs['unites']['v'] = 15
                compteurs['batiments']['T'] = 3
                compteurs['batiments']['B'] = 2
                compteurs['batiments']['S'] = 2
                compteurs['batiments']['A'] = 2

    def draw_resources(self):
        x_barre_base = 100  # Position de départ en X pour la première colonne
        y_barre_base = 40   # Position de départ en Y pour la première ligne

        espacement_horizontal = barre_width +200  # Espacement entre les colonnes
        espacement_vertical = 200    # Espacement entre les lignes

        total_images = len(self.barres)
        total_images_barre_builds = len(self.barre_builds)

        for index, (joueur, compteurs) in enumerate(compteurs_joueurs.items()):
            # Calcul de la position en X et Y pour chaque joueur
            colonne = index % 2  # 0 pour la première colonne, 1 pour la seconde
            ligne = index // 2   # Numéro de la ligne

            x_barre = x_barre_base + colonne * espacement_horizontal
            y_barre = y_barre_base + ligne * espacement_vertical

            #print (x_barre, y_barre)

            # Affiche les ressources (f1_active)
            if self.f1_active:
                self.barres[0].barre(DISPLAYSURF, x_barre, y_barre)
                for i, barre in enumerate(self.barres):
                    type = ["w", "g", "f", "U"][i]
                    barre.draw(DISPLAYSURF, x_barre, y_barre, self.compteur[joueur]['ressources'][type], i, total_images)

            # Affiche les unités (f2_active)
            if self.f2_active:
                for barre_unit in self.barres:
                    barre_unit.barre_units(DISPLAYSURF, x_barre, y_barre + barre_height)
                for i, barre in enumerate(self.barre_units):
                    type = ["v", "s", "h", "a"][i]
                    barre.draw_barre_units(DISPLAYSURF, x_barre, y_barre + barre_height, self.compteur[joueur]['unites'][type], i, total_images)

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
            print(self.tile_map.position_initiale)
            #print("avant",self.cam_x, self.cam_y)

            # Récupération de la position du joueur
            y, x = self.tile_map.position_initiale  # Assurez-vous de l'ordre ici (col, row)
            half_size = size // 2  # Assurez-vous que la taille de la carte est correctement définie

            # Décalage centré pour le joueur
            centered_col = y - half_size
            centered_row = x - half_size
            print("centered", centered_col, centered_row)

            # Conversion en coordonnées isométriques
            cart_x = centered_row * tile_grass.width_half
            cart_y = centered_col * tile_grass.width_half
            print("cart", cart_x, cart_y)

            iso_x = cart_x - cart_y  # Ne pas soustraire cam_x ici
            iso_y = (cart_x + cart_y) / 2  # Ne pas soustraire cam_y ici
            print("iso",iso_x, iso_y)

            self.cam_x = iso_x - (screen_width // 2) + tile_grass.width_half
            self.cam_y = iso_y - (screen_height // 2)

            print("Caméra après ajustement:", self.cam_x, self.cam_y)

        else:

            iso_x = self.cam_x + (screen_width // 2) - tile_grass.width_half
            iso_y = self.cam_y + (screen_height // 2)
            print("iso avant", iso_x, iso_y)

            # Conversion des coordonnées isométriques en coordonnées cartésiennes
            cart_x = (iso_x + 2 * iso_y) / 2
            cart_y = (2 * iso_y - iso_x) / 2   # Formule inverse pour obtenir cart_y

            print("cart avant", cart_x, cart_y)

            # Conversion des coordonnées cartésiennes en indices de la matrice
            # Récupération des indices de la matrice
            half_size = len(self.tile_map.get_map_data()) // 2  # Taille centrée de la carte

            centered_col = int(cart_y / tile_grass.height_half)  # Indice de la colonne
            centered_row = int(cart_x / tile_grass.width_half)  # Indice de la ligne

            print("tuile",tile_grass.height_half, tile_grass.width_half )

            print("centerer avant", centered_row, centered_col)

            # Récupération des coordonnées de la matrice
            y = centered_row + half_size  # Ajustement en fonction de half_size
            x = centered_col + half_size  # Ajustement en fonction de half_size

            print(x,y)

            self.tile_map.position_initiale = x,y
            # Ouvre le terminal dans un nouveau thread
            self.terminal_active = True
            terminal_thread = threading.Thread(target=curses.wrapper, args=(self.draw_map_in_terminal,))
            terminal_thread.daemon = True
            terminal_thread.start()


    def run(self):
            """Boucle principale du jeu."""
            running = True
            load = False
            pygame.display.set_caption("Carte et mini-carte")




            while running:
                events = pygame.event.get()
                for event in events:
                    if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and event.key == K_F1:
                        self.f1_active = not self.f1_active

                    if event.type == KEYDOWN and event.key == K_F2:
                        self.f2_active = not self.f2_active

                    if event.type == KEYDOWN and event.key == K_F3:
                        self.f3_active = not self.f3_active

                    if event.type == KEYDOWN and event.key == K_p:
                        self.ouvrir_terminal()

                    if self.menu_active:
                        self.handle_menu_events(event)
                    else :
                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            if not self.menu_active:
                                self.handle_mini_map_click(mouse_pos)
                if self.menu_active:
                    self.show_menu()
                else:


                    pygame.display.update()
                    DISPLAYSURF.fill(BLACK)
                    self.tile_map.render(DISPLAYSURF, self.cam_x, self.cam_y)
                    self.draw_mini_map(DISPLAYSURF)

                    keys = pygame.key.get_pressed()
                    self.handle_camera_movement(keys)


                    self.draw_resources()

                    '''
                    position1 = self.unit.conversion(60,110)
                    position1 = (position1[0] - self.cam_x + units_images['v'].get_width() // 2 ,
                                position1[1] - units_images['v'].height // 2 - self.cam_y)
                    DISPLAYSURF.blit(units_images['v'], position1)
                    
                    print("test",position1)
                    
                    print("debut")
                    if self.swordsman.affichage(self.cam_x, self.cam_y, self.n)!= None :
                        print("appel", self.swordsman.affichage(self.cam_x, self.cam_y, self.n))
                        position2 = self.swordsman.affichage(self.cam_x, self.cam_y, self.n)

                        print("pos2",position2)

                        DISPLAYSURF.blit(units_images['v'], position2)
                        print("fin")
                    '''

                    #self.unit.affichage()
                    self.buildings.affichage()
                    #print("\n",tuiles)




                    #if self.swordsman.affichage(self.cam_x, self.cam_y, self.n) != None:
                       #for i

                    #self.unit.affichage(self.n)
                    pygame.display.flip()


                    #self.swordsman.affichage(self.n,self.cam_x, self.cam_y,'images/epeiste.png')
                    #print (units_images)


                pygame.display.update()
                FPSCLOCK.tick(60)

