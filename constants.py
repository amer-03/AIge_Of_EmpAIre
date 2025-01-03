import pygame
import numpy as np


class Tile:
    def __init__(self, image_path, width, height):
        # Chargez l'image et appliquez le redimensionnement en width x height pixels
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))  # Redimensionne l'image

        # Stockez les dimensions spécifiées
        self.width = width
        self.height = height
        self.width_half = width // 2
        self.height_half = height // 2

pygame.init()





info = pygame.display.Info()
screen_width = info.current_w  # Largeur de l'écran
screen_height = info.current_h  # Hauteur de l'écran

DISPLAYSURF = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
FPSCLOCK = pygame.time.Clock()

minimap_size = 50
map_size = 120

barre_width = 700  # Largeur de la barre
barre_height = 80  # Hauteur de la barre

barre_units_width= 700
barre_units_height = 40


tile_grass = Tile('images/cube_grass.png', 64, 64)
tile_wood = Tile('images/cube_tree3.png', 64, 128)
tile_gold = Tile('images/cube_rocky2.png', 64, 80)



swordsman_image = pygame.image.load("images/epeiste.png")  # Remplace "swordsman.png" par le nom de ton fichier
swordsman_image = pygame.transform.scale(swordsman_image, (32, 32))


compteurs_joueurs = {}
units_images = {
    'v': Tile("images/villageois.webp", 32, 32), # Villageois
    's': Tile("images/epeiste.png", 32, 32),      # Épéiste
    'h': Tile("images/cavalier.png", 32, 32),     # Cavalier
    'a': Tile("images/archer.png", 30, 30)        # Archer
}

builds_images = {
    'T': {'tile': Tile("images/Town_Center.webp", 200, 128), 'taille': 4},
    'H': {'tile': Tile("images/House.webp", 90, 70), 'taille': 2},  # Exemple de taille 1
    'C': {'tile': Tile("images/Camp.png",  90, 70), 'taille': 2},
    'F': {'tile': Tile("images/Farm - Copie.png",  90, 70), 'taille': 2},
    'B': {'tile': Tile("images/Barracks.png", 128, 100), 'taille': 3},  # Exemple de taille 2
    'S': {'tile': Tile("images/Stable.png", 128, 100), 'taille': 3},
    'A': {'tile': Tile("images/Archery Range.png", 128, 100), 'taille': 3},  # Exemple de taille 3
    'K': {'tile': Tile("images/Keep.png", 64, 64), 'taille': 1}
}
size=120

tuiles = {}
compteurs_unites = {}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128,128,128)

test_posi = []

map_data = np.full((size, size), " ")