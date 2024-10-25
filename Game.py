import pygame
import sys
import json
from pygame.locals import *
from constants import *
from Tile import Tile
from TileMap import TileMap
from Barre_ressource import Barre_ressources


class Game:
    """Classe principale gérant le jeu."""

    def __init__(self, screen_width, screen_height, map_size, minimap_size):


        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll_speed = 30
        self.mini_scroll_speed_x = 30
        self.mini_scroll_speed_y = 110




        # Charger les tuiles
        self.tile_grass = Tile('cube_grass.png', 64, 64)
        self.tile_wood = Tile('cube_grass - Copie.png', 128, 128)
        self.tile_gold = Tile('cube_rocky2.png', 64, 64)


        # Sélection de la carte
        self.map_size = map_size
        self.tile_map = None

        self.mini_map_size_x = 490  # Largeur de la mini-carte
        self.mini_map_size_y = 270  # Hauteur de la mini-carte  # Taille carrée de la mini-carte
        self.mini_map_scale = 4 # Échelle de réduction de la mini-carte

        self.cam_scale_x = self.mini_map_size_x / (self.map_size * self.tile_grass.width_half)
        self.cam_scale_y = self.mini_map_size_y / (self.map_size * self.tile_grass.height_half)
        self.rect_x = 0
        self.rect_y = 0
        # Dimensions du rectangle représentant la caméra, proportionnelles à l'écran
        self.rect_width = (self.screen_width * self.cam_scale_x) * 0.5  # Réduire la largeur du rectangle
        self.rect_height = (self.screen_height * self.cam_scale_y) * 0.9  # Réduire la hauteur du rectangle

        # Initialisation des coordonnées de la caméra
        self.cam_x, self.cam_y = self.center_camera_on_tile()
        self.cam_mini_x, self.cam_mini_y = self.center_camera_on_tile()


        self.barre_ressources = Barre_ressources
        self.compteur = 0

        self.barres = [
            Barre_ressources("bois_barre.png", "Compteur Bois", 24),
            Barre_ressources("or_barre.png", "Compteur Or", 24),
            Barre_ressources("food_barre.png", "Compteur Food", 24),
            Barre_ressources("entite.png", "Compteur Fer", 24)

        ]
        self.compteurs = {
            "bois": 0,
            "or": 0,
            "food": 0,
            "fer": 0,

        }  # Compteurs pour chaque image



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

        # Calculer la position de la caméra pour centrer cette tuile sur l'écran
        cam_x = (iso_x - self.screen_width // 2) + tile_width_half
        cam_y = -(iso_y + self.screen_height // 2 )

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

    def draw_mini_map(self, display_surface):
        """Affiche une version réduite de la carte en bas à gauche, orientée de manière isométrique."""
        losange_surface = pygame.Surface((self.mini_map_size_x, self.mini_map_size_y), pygame.SRCALPHA)
        losange_surface.fill((0, 0, 0, 0))  # Remplir de transparent

        mini_map_surface = pygame.Surface((self.mini_map_size_x, self.mini_map_size_y), pygame.SRCALPHA)
        mini_map_surface.fill((0, 0, 0, 0))  # Fond transparent
        tile_width_half = 1
        tile_height_half = 1

        for row in range(self.map_size):
            for col in range(self.map_size):
                tile_type = self.tile_map.map_data[row][col]

                # Couleur des tuiles sur la mini-carte
                if tile_type == " ":
                    color = (34, 139, 34)  # Vert pour l'herbe
                elif tile_type == "W":
                    color = (139, 69, 19)  # Marron pour le bois
                elif tile_type == "G":
                    color = (255, 215, 0)  # Jaune pour l'or
                elif tile_type == "T":
                    color = (128, 128, 128)  # Gris pour le bloc spécial

                # Transformation isométrique
                centered_col = col - (self.map_size // 2)
                centered_row = row - (self.map_size // 2)

                # Conversion des coordonnées cartésiennes en coordonnées isométriques pour la mini-carte
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

        # Dessiner le contour noir du losange
        pygame.draw.polygon(losange_surface, (0, 0, 0), losange_points, 2)  # Contour noir de 2 pixels
        """
                    A SUPPRIMER 
        print("rectx",self.cam_mini_x, self.cam_mini_y)

        self.rect_x = (self.cam_mini_x + (self.screen_width // 2)) * self.cam_scale_x / 2 + self.mini_map_size_x // 2 - self.rect_width / 2
        self.rect_y = (self.cam_mini_y + (self.screen_height // 2)) * self.cam_scale_y / 4 + self.mini_map_size_y // 2 - self.rect_height / 2

        pygame.draw.rect(mini_map_surface, (255,0 , 0), (self.rect_x, self.rect_y, self.rect_width, self.rect_height), 1)
        """
        losange_surface.blit(mini_map_surface, (0, 0))  # Positionner la mini-carte sur le losange

        # Afficher le losange sur l'écran principal
        display_surface.blit(losange_surface, (
            self.screen_width - self.mini_map_size_x - 10, self.screen_height - self.mini_map_size_y - 10))

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


    def handle_mini_camera_movement(self, keys):
        """Gère le mouvement de la caméra avec des limites."""
        min_cam_x, min_cam_y, max_cam_x, max_cam_y = self.calculate_camera_limits()

        if keys[K_q]:
            self.cam_mini_x = max(self.cam_mini_x - self.mini_scroll_speed_x, min_cam_x)
        if keys[K_d]:
            self.cam_mini_x = min(self.cam_mini_x + self.mini_scroll_speed_x, max_cam_x)
        if keys[K_z]:
            self.cam_mini_y = max(self.cam_mini_y - self.mini_scroll_speed_y, min_cam_y*3)
        if keys[K_s]:
            self.cam_mini_y = min(self.cam_mini_y + self.mini_scroll_speed_y, max_cam_y*5.05)

    def handle_mini_map_click(self, mouse_pos):
        """Gère le clic sur la mini-carte et déplace la caméra."""
        # Définir la zone de la mini-carte
        mini_map_rect = pygame.Rect(self.screen_width - self.mini_map_size_x - 10,
                                    self.screen_height - self.mini_map_size_y - 10,
                                    self.mini_map_size_x, self.mini_map_size_y)

        # Vérifier si le clic est dans la mini-carte
        if mini_map_rect.collidepoint(mouse_pos):
            # Calculer les coordonnées dans la mini-carte
            mini_map_x = mouse_pos[0] - (self.screen_width - self.mini_map_size_x - 10)
            mini_map_y = mouse_pos[1] - (self.screen_height - self.mini_map_size_y - 10)

            # Échelle entre la mini-carte et la carte principale
            scale_x = self.map_size * (self.tile_grass.width_half*2) / self.mini_map_size_x
            scale_y = self.map_size * self.tile_grass.height_half / self.mini_map_size_y

            # Conversion en coordonnées du monde principal
            world_x = int((mini_map_x - self.mini_map_size_x //2) * scale_x)
            world_y = int((mini_map_y - self.mini_map_size_y // 2) * scale_y)


            # Mise à jour de la caméra pour centrer sur la position cliquée
            self.cam_x = world_x - self.screen_width // 2
            self.cam_y = world_y - self.screen_height // 2
            """
            A SUPPRIMER 
            self.cam_mini_x = int((mini_map_x - self.mini_map_size_x // 2) * scale_x)
            self.cam_mini_y = int((mini_map_y - self.mini_map_size_y // 2) * scale_y)

            # Mise à jour du rectangle rouge pour qu'il soit centré sur la position cliquée
            self.rect_x = (self.cam_mini_x / scale_x) + self.mini_map_size_x // 2 - self.rect_width // 2
            self.rect_y = (self.cam_mini_y / scale_y) + self.mini_map_size_y // 2 - self.rect_height // 2
            """

    def run(self):
            """Boucle principale du jeu."""
            running = True
            menu = True
            load = False
            display_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("Carte et mini-carte")

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
                                #self.tile_map.open_second_terminal()
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

                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            # Obtenir la position de la souris
                            mouse_pos = pygame.mouse.get_pos()

                            # Vérifier si la souris est sur une option de menu
                            if card1_rect.collidepoint(mouse_pos):
                                self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold)
                                # self.tile_map.open_second_terminal()
                                menu = False
                            elif card2_rect.collidepoint(mouse_pos):
                                self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold)
                                # self.tile_map.open_second_terminal()
                                menu = False
                            elif card3_rect.collidepoint(mouse_pos):
                                self.tile_map = TileMap(self.map_size, self.tile_grass, self.tile_wood, self.tile_gold)
                                # self.tile_map.open_second_terminal()
                                menu = False
                            elif load_data_rect.collidepoint(mouse_pos):
                                print("Chargement des données sauvegardées")
                                menu = False
                                load = True

                if event.type == MOUSEBUTTONDOWN and event.button == 1 and not menu:
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_mini_map_click(mouse_pos)


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
                    self.handle_mini_camera_movement(keys)

                    DISPLAYSURF.fill((0, 0, 0))  # Effacer l'écran
                    self.tile_map.render(DISPLAYSURF, self.cam_x, self.cam_y)
                    self.draw_mini_map(display_surface)
                    x_barre = (self.screen_width - self.barres[0].barre_width) // 2
                    y_barre = 40

                    # Dessiner la barre noire (rectangle centré)
                    self.barres[0].barre(DISPLAYSURF, x_barre, y_barre)

                    # Afficher chaque image et texte à l'intérieur de la barre
                    total_images = len(self.barres)
                    for i, barre in enumerate(self.barres):
                        ressource = ["bois", "or", "food", "or"][i]
                        barre.draw(DISPLAYSURF, x_barre, y_barre, self.compteurs[ressource], i, total_images)

                pygame.display.update()
                FPSCLOCK.tick(60)

