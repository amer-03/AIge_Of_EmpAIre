import pygame
from pygame.locals import *
import numpy as np
import random
from math import *
import subprocess
import os

pygame.init()

# Configuration de l'écran et des FPS
screen_width = pygame.display.Info().current_h
screen_height = pygame.display.Info().current_w
DISPLAYSURF = pygame.display.set_mode((screen_width,screen_height), pygame.FULLSCREEN)
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
        self.object_layer = np.full((size, size), None)  # Couche supplémentaire pour les objets comme les arbres
        self.tile_grass = tile_grass
        self.tile_wood = tile_wood
        self.tile_gold = tile_gold
        self.tile_test = tile_test
        self.add_wood_patches()
        self.add_gold_patches()
        self.add_special_block()

    def add_wood_patches(self):
        """Ajoute des paquets de bois (W) sur la carte."""
        num_patches = random.randint(30, 40)
        min_patch_size = 3
        max_patch_size = 7

        for _ in range(num_patches):
            patch_size = random.randint(min_patch_size, max_patch_size)
            start_x = random.randint(0, self.size - 1)
            start_y = random.randint(0, self.size - 1)

            wood_tiles = [(start_x, start_y)]
            while len(wood_tiles) < patch_size:
                tile_x, tile_y = random.choice(wood_tiles)
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Choisir une direction
                new_x = tile_x + direction[0]
                new_y = tile_y + direction[1]

                if 0 <= new_x < self.size and 0 <= new_y < self.size:
                    if self.object_layer[new_y][new_x] is None:  # Placer du bois si l'objet est vide
                        self.object_layer[new_y][new_x] = "W"
                        wood_tiles.append((new_x, new_y))

    def add_gold_patches(self):
        """Ajoute des paquets d'or (G) sur la carte."""
        num_patches = random.randint(5, 10)
        min_patch_size = 2
        max_patch_size = 5

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
                # Affichage de la couche sol
                tile_type = self.map_data[row][col]
                if tile_type == " ":
                    tile = self.tile_grass
                    offset_y = 0
                elif tile_type == "G":
                    tile = self.tile_gold
                    offset_y = tile.height - self.tile_grass.height
                elif tile_type == "T":
                    tile = self.tile_test
                    offset_y = tile.height - self.tile_grass.height

                centered_col = col - half_size  # Décalage en X
                centered_row = row - half_size  # Décalage en Y

                cart_x = centered_col * self.tile_grass.width_half
                cart_y = centered_row * self.tile_grass.height_half

                iso_x = (cart_x - cart_y) - cam_x
                iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y

                display_surface.blit(tile.image, (iso_x, iso_y))

                # Affichage des objets au-dessus du sol (par exemple, les arbres)
                object_type = self.object_layer[row][col]
                if object_type == "W":
                    tile = self.tile_wood
                    iso_y -= tile.height - self.tile_grass.height
                    display_surface.blit(tile.image, (iso_x, iso_y))

    def add_special_block(self):
        """Ajoute un bloc spécial au centre de la carte."""
        center_x = self.size // 2
        center_y = self.size // 2
        self.map_data[center_y][center_x] = "T"  # Placer un bloc spécial au centre
