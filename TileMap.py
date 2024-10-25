import pygame
from Tile import Tile
import numpy as np
import random
import subprocess
import os



class TileMap:
    """Classe gérant la carte des tuiles."""
    def __init__(self, size, tile_grass, tile_wood, tile_gold):
        self.size = size
        self.map_data = np.full((size, size), " ")  # Remplir la carte d'herbe
        self.tile_grass = tile_grass
        self.tile_wood = tile_wood
        self.tile_gold = tile_gold
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



    def open_second_terminal(self):
        """Ouvre un nouveau terminal pour suivre l'affichage de la carte."""
        if os.name == 'posix':  # Si tu es sur un système Unix (Linux/MacOS)
            subprocess.Popen(['gnome-terminal', '--', '--zoom=0.8', 'tail', '-f', 'map_output.txt'])
        elif os.name == 'nt':  # Si tu es sur Windows
            subprocess.Popen(['start', 'cmd', '/K', 'type', 'map_output.txt'], shell=True)


    def add_special_block(self):
        """Ajoute un bloc spécial au centre de la carte."""
        center_x = self.size // 2
        center_y = self.size // 2

        print(center_x, center_y)
        self.map_data[center_y][center_x] = "T"  # Placer un bloc spécial au centre