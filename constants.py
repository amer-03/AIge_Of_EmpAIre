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
tile_wood = Tile('images/cube_three.png', 64, 128)
tile_gold = Tile('images/cube_rocky2.png', 64, 64)



swordsman_image = pygame.image.load("images/epeiste.png")  # Remplace "swordsman.png" par le nom de ton fichier
swordsman_image = pygame.transform.scale(swordsman_image, (32, 32))


compteurs_joueurs = {}
units_images = {
    'v': Tile("images/villageois.webp", 32, 32), # Villageois
    's': Tile("images/epeiste.png", 32, 32),      # Épéiste
    'h': Tile("images/cavalier.png", 32, 32),     # Cavalier
    'a': Tile("images/archer.png", 30, 30)        # Archer
}


units_images_test = {
    'v': {
        'image': Tile("images/villageois.webp", 32, 32),
        'cout': {'Gold': 0, 'Food': 50, 'Wood': 0},
        'hp': 25,
        'temps_entrainement': 25,
        'attaque': 2,
        'vitesse': 0.8
    },
    's': {  # Épéiste
        'image': Tile("images/epeiste.png", 32, 32),
        'cout': {'Gold': 20, 'Food': 50, 'Wood': 0},
        'hp': 40,
        'temps_entrainement': 20,
        'attaque': 4,
        'vitesse': 0.9
    },
    'h': {  # Cavalier
        'image': Tile("images/cavalier.png", 32, 32),
        'cout': {'Gold': 20, 'Food': 80, 'Wood': 0},
        'hp': 45,
        'temps_entrainement': 30,
        'attaque': 4,
        'vitesse': 1.2
    },
    'a': {  # Archer
        'image': Tile("images/archer.png", 30, 30),
        'cout': {'Gold': 45, 'Food': 0, 'Wood': 25},
        'hp': 30,
        'temps_entrainement': 35,
        'attaque': 4,
        'vitesse': 1
    }
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


builds_images_test = {
    'T': {
        'tile': Tile("images/Town_Center.webp", 200, 128),
        'taille': 4,
        'cost': {'Gold': 0, 'Wood': 350, 'Food': 0},
        'build_time': 150,  # Temps en secondes
        'hp': 1000
    },
    'H': {
        'tile': Tile("images/House.webp", 90, 70),
        'taille': 2,
        'cost': {'Gold': 0, 'Wood': 25, 'Food': 0},
        'build_time': 25,
        'hp': 200
    },
    'C': {
        'tile': Tile("images/Camp.png", 90, 70),
        'taille': 2,
        'cost': {'Gold': 0, 'Wood': 100, 'Food': 0},
        'build_time': 25,
        'hp': 200
    },
    'F': {
        'tile': Tile("images/Farm - Copie.png", 90, 70),
        'taille': 2,
        'cost': {'Gold': 0, 'Wood': 60, 'Food': 0},
        'build_time': 10,
        'hp': 100,
        'nombre': 300

    },
    'B': {
        'tile': Tile("images/Barracks.png", 128, 100),
        'taille': 3,
        'cost': {'Gold': 0, 'Wood': 175, 'Food': 0},
        'build_time': 50,
        'hp': 500
    },
    'S': {
        'tile': Tile("images/Stable.png", 128, 100),
        'taille': 3,
        'cost': {'Gold': 0, 'Wood': 175, 'Food': 0},
        'build_time': 50,
        'hp': 500
    },
    'A': {
        'tile': Tile("images/Archery Range.png", 128, 100),
        'taille': 3,
        'cost': {'Gold': 0, 'Wood': 175, 'Food': 0},
        'build_time': 50,
        'hp': 500
    },
    'K': {
        'tile': Tile("images/Keep.png", 64, 64),
        'taille': 1,
        'cost': {'Gold': 125, 'Wood': 35, 'Food': 0},
        'build_time': 80,
        'hp': 800
    }
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