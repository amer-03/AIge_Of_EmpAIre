import pygame
import numpy as np
import curses

class Tile:
    def __init__(self, image_path, width, height):
        self.image1 = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image1, (width, height))
        self.width = width
        self.height = height
        self.width_half = width // 2
        self.height_half = height // 2


#initialisation de pygame
pygame.init()
info = pygame.display.Info()
screen_width = info.current_w #-500  # Largeur de l'écran
screen_height = info.current_h #-500  # Hauteur de l'écran
DISPLAYSURF = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
FPSCLOCK = pygame.time.Clock()


#classe de la tuile 
tile_grass = Tile('images/cube_grass.png', 64, 64)
tile_wood = Tile('images/cube_three.png', 64, 128)
tile_gold = Tile('images/cube_rocky2.png', 64, 64)


size = 120
half_size = size//2

map_data = np.full((size, size), " ")

barre_width = screen_width//2.5  # Largeur de la barre
barre_height = screen_height//13.5 # Hauteur de la barre

barre_units_width= screen_width//2.5
barre_units_height = screen_height//27



swordsman_image = pygame.image.load("images/epeiste.png")  # Remplace "swordsman.png" par le nom de ton fichier
swordsman_image = pygame.transform.scale(swordsman_image, (32, 32))



compteurs_joueurs = {}

units_dict = {
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

builds_dict = {
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


tuiles = {}
compteurs_unites = {}

GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128,128,128)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BROWN = (139, 69, 19)
PINK = (255, 105, 180)

PLAYER_COLORS = {
    "joueur_1": RED,       # Rouge
    "joueur_2": GREEN,     # Vert
    "joueur_3": YELLOW,    # Jaune
    "joueur_4": BLUE,      # Bleu
    "joueur_5": ORANGE,    # Orange
    "joueur_6": PURPLE,    # Violet
    "joueur_7": CYAN,      # Cyan
    "joueur_8": MAGENTA,   # Magenta
    "joueur_9": BROWN,     # Marron
    "joueur_10": PINK      # Vert clair
}

MAP_COLORS = {
    "joueur_1": (1, curses.COLOR_BLACK),
    "joueur_2": (2, curses.COLOR_BLACK),
    "joueur_3": (3, curses.COLOR_BLACK),
    "joueur_4": (4, curses.COLOR_BLACK),
    "joueur_5": (202, curses.COLOR_BLACK),
    "joueur_6": (129, curses.COLOR_BLACK),
    "joueur_7": (51, curses.COLOR_BLACK),
    "joueur_8": (201, curses.COLOR_BLACK),
    "joueur_9": (94, curses.COLOR_BLACK),
    "joueur_10": (218, curses.COLOR_BLACK),
}

