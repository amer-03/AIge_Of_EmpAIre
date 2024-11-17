import pygame
import random
from constants import *
import keyboard
import curses
import pygame
import threading
import time

class TileMap:
    """Classe gérant la carte des tuiles."""
    def __init__(self):
        self.add_wood_patches()
        self.position_initiale = (size // 2, size // 2)

    def mode(self,mode):
        if mode == "patches":
            self.add_gold_patches()
        elif mode == "middle" :
           self.add_gold_middle()


    def add_wood_patches(self):
        """Ajoute des paquets de bois (W) sur la carte."""
        num_patches = random.randint(10, 20)
        min_patch_size = 3
        max_patch_size = 7

        for _ in range(num_patches):
            patch_size = random.randint(min_patch_size, max_patch_size)
            start_x = random.randint(0, size - 1)
            start_y = random.randint(0, size - 1)

            wood_tiles = [(start_x, start_y)]
            map_data[start_y][start_x] = "W"  # Placer la première tuile de bois

            while len(wood_tiles) < patch_size:
                tile_x, tile_y = random.choice(wood_tiles)
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Choisir une direction
                new_x = tile_x + direction[0]
                new_y = tile_y + direction[1]

                if 0 <= new_x < size and 0 <= new_y < size:
                    if map_data[new_y][new_x] == " ":  # Placer du bois si la case est d'herbe
                        map_data[new_y][new_x] = "W"
                        wood_tiles.append((new_x, new_y))

    def add_gold_patches(self):
        """Ajoute des paquets d'or (G) sur la carte."""
        num_patches = random.randint(5, 10)  # Nombre de paquets d'or à générer
        min_patch_size = 2  # Taille minimale d'un paquet
        max_patch_size = 5  # Taille maximale d'un paquet

        for _ in range(num_patches):
            patch_size = random.randint(min_patch_size, max_patch_size)
            start_x = random.randint(0, size - 1)
            start_y = random.randint(0, size - 1)

            gold_tiles = [(start_x, start_y)]
            if map_data[start_y][start_x] == " ":
                map_data[start_y][start_x] = "G"  # Placer la première tuile d'or

            while len(gold_tiles) < patch_size:
                tile_x, tile_y = random.choice(gold_tiles)
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # (dx, dy)
                new_x = tile_x + direction[0]
                new_y = tile_y + direction[1]

                if 0 <= new_x < size and 0 <= new_y < size:
                    if map_data[new_y][new_x] == " ":
                        map_data[new_y][new_x] = "G"
                        gold_tiles.append((new_x, new_y))


    def add_gold_middle(self):
        """Ajoute un paquet d'or (G) au centre de la carte."""
        center_x = size // 2
        center_y = size // 2
        max_patch_size = 5  # Taille maximale d'un paquet

        # Placer un paquet d'or autour du centre
        for dx in range(-max_patch_size // 2, max_patch_size // 2 + 1):
            for dy in range(-max_patch_size // 2, max_patch_size // 2 + 1):
                new_x = center_x + dx
                new_y = center_y + dy

                # Vérifier si la nouvelle position est dans la carte et vide
                if 0 <= new_x < size and 0 <= new_y < size:
                    map_data[new_y][new_x] = "G"  # Placer une tuile d'or

    def ajouter_unite(self,row, col, unite):
        # Ajoute l'unité si elle n'est pas déjà présente dans la cellule
        map_data[row][col].append(unite)

    def afficher_unite(self,tile_type, cart_x, cart_y, cam_x, cam_y, tile_grass, display_surface):
        # Obtenir l'image correspondant au type d'unité
        unit_tile = units_images.get(tile_type)
        if not unit_tile:
            return  # Si l'image n'existe pas, ne rien faire

        # Calculer les offsets
        offset_x = tile_grass.width_half - unit_tile.width // 2
        offset_y = tile_grass.height_half - unit_tile.height // 2

        # Recalculer les coordonnées isométriques pour l'unité
        iso_x = (cart_x - cart_y) - cam_x + offset_x
        iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y

        #print("units", iso_x,iso_y)

        # Afficher l'unité
        display_surface.blit(unit_tile.image, (iso_x, iso_y))

    def afficher_buildings(self, tile_type, grid_x, grid_y, cam_x, cam_y, tile_grass, display_surface):
        tuile = tuiles.get((grid_x, grid_y))
        if not tuile or not tuile.get('unites'):
            return



        #print(grid_x,grid_y)

        for joueur, buildings in tuile['unites'].items():
            for tile_type, data in buildings.items():
                if isinstance(data, dict) and data.get('principal'):
                    # Vérifiez si les données du bâtiment existent
                    if tile_type not in builds_images:
                        return

                    # Récupérer l'image et les dimensions
                    unit_tile = builds_images[tile_type]['tile']
                    building_width = unit_tile.width  # Largeur du bâtiment
                    building_height = unit_tile.height  # Hauteur du bâtiment

                    # Calculer les coordonnées cartésiennes de la tuile
                    centered_col = grid_y - size // 2  # Décalage en X (par rapport à la grille)
                    centered_row = grid_x - size // 2  # Décalage en Y (par rapport à la grille)

                    offset_y =  tile_grass.height_half-unit_tile.height
                    offset_x = tile_grass.width_half - unit_tile.width

                    # Calcul des coordonnées cartésiennes
                    cart_x = centered_col * tile_grass.width_half
                    cart_y = centered_row * tile_grass.height_half

                    # Conversion en coordonnées isométriques
                    iso_x = (cart_x - cart_y) - cam_x  #- offset_x
                    iso_y = (cart_x + cart_y) / 2 - cam_y + offset_y


                    display_surface.blit(unit_tile.image, (iso_x, iso_y))



    def render(self, display_surface, cam_x, cam_y):
        """Affiche la carte en fonction de la position de la caméra, centrée au milieu."""
        half_size = size // 2  # La moitié de la taille de la carte

        for row in range(size):
            for col in range(size):
                tile_type = map_data[row][col]
                if tile_type == " ":
                    tile = tile_grass
                    offset_y = 0

                elif tile_type == "W":
                    tile = tile_wood
                    offset_y = tile.height - tile_grass.height
                    if (row, col) not in tuiles:
                       tuiles[(row, col)] = {'unites': None}  # Initialiser 'unites' à None

                    tuiles[(row, col)]['unites'] = str(tile_type)
                elif tile_type == "G":
                    tile = tile_gold
                    #print(tile_type)
                    offset_y = tile.height - tile_grass.height
                    if (row, col) not in tuiles:
                        tuiles[(row, col)] = {'unites': None}  # Initialiser 'unites' à None

                    tuiles[(row, col)]['unites'] = str(tile_type)


                # Coordonnées cartésiennes centrées
                centered_col = col - half_size  # Décalage en X
                centered_row = row - half_size  # Décalage en Y

                # Conversion en coordonnées isométriques
                cart_x = centered_col * tile_grass.width_half
                cart_y = centered_row * tile_grass.height_half

                iso_x = (cart_x - cart_y) - cam_x
                iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y

                #print ("test")
                display_surface.blit(tile.image, (iso_x, iso_y))
                display_surface.blit(tile_wood.image, (60, 10))
                if tile_type in ["v", "s", "h", "a"]:
                    #print(tile_type)
                    self.afficher_unite(tile_type, cart_x, cart_y, cam_x, cam_y, tile_grass, display_surface)

                if tile_type in ["T", "H", "C", "F", "B", "S", "A", "K"]:
                    self.afficher_buildings(tile_type, row, col, cam_x, cam_y, tile_grass, display_surface)




                """
                if tile_type == "v":  # Unité villageois
                    unit_tile = units_images['v']  # Assurez-vous que 'v' correspond à l'image du villageois
                    offset_x = tile_grass.width_half - unit_tile.width // 2
                    offset_y = tile_grass.height_half - unit_tile.height // 2

                    # Recalculer les coordonnées isométriques pour l'unité
                    iso_x = (cart_x - cart_y) - cam_x + offset_x
                    iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y   # Déplacer l'unité juste au-dessus de l'herbe

                    # Afficher l'unité (villageois)
                    display_surface.blit(unit_tile.image, (iso_x, iso_y))

                if tile_type == "s":
                    unit_tile = units_images['s']
                    offset_x = tile_grass.width_half - unit_tile.width // 2
                    offset_y = tile_grass.height_half - unit_tile.height // 2

                    # Recalculer les coordonnées isométriques pour l'unité
                    iso_x = (cart_x - cart_y) - cam_x + offset_x
                    iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y

                    # Afficher l'unité (villageois)
                    display_surface.blit(unit_tile.image, (iso_x, iso_y))

                if tile_type == "h":
                    unit_tile = units_images['h']
                    offset_x = tile_grass.width_half - unit_tile.width // 2
                    offset_y = tile_grass.height_half - unit_tile.height // 2

                    # Recalculer les coordonnées isométriques pour l'unité
                    iso_x = (cart_x - cart_y) - cam_x + offset_x
                    iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y

                    # Afficher l'unité (villageois)
                    display_surface.blit(unit_tile.image, (iso_x, iso_y))

                if tile_type == "a":
                    unit_tile = units_images['a']
                    offset_x = tile_grass.width_half - unit_tile.width // 2
                    offset_y = tile_grass.height_half - unit_tile.height // 2

                    # Recalculer les coordonnées isométriques pour l'unité
                    iso_x = (cart_x - cart_y) - cam_x + offset_x
                    iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y

                    # Afficher l'unité (villageois)
                    display_surface.blit(unit_tile.image, (iso_x, iso_y))

                """



    def move_player(self, direction):
        x, y = self.position_initiale
        map_data[y][x] = " "  # Efface l'ancienne position

        if direction == 'up' and y > 0:
            y -= 1
        elif direction == 'down' and y < size - 1:
            y += 1
        elif direction == 'left' and x > 0:
            x -= 1
        elif direction == 'right' and x < len(map_data[y]) - 1:
            x += 1

        self.position_initiale = (x, y)


    def get_map_data(self):
        """Retourne la carte actuelle pour affichage."""
        return map_data



