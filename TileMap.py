import pygame
import random
from constants import *
from Units import Units
from Coordinates import Coordinates
from Villager import Villager


class TileMap:
    """Classe gérant la carte des tuiles."""

    def __init__(self):
        # self.add_wood_patches()
        self.position_initiale = (size // 2, size // 2)

    def mode(self, mode):
        if mode == "patches":
            self.add_gold_patches()
        elif mode == "middle":
            self.add_gold_middle()

    def add_wood_patches(self):
        """Ajoute des paquets de bois (W) sur la carte."""
        # print("wood")
        num_patches = random.randint(10, 20)
        min_patch_size = 7
        max_patch_size = 15

        for _ in range(num_patches):
            patch_size = random.randint(min_patch_size, max_patch_size)
            start_x = random.randint(0, size - 1)
            start_y = random.randint(0, size - 1)
            wood_tiles = [(start_x, start_y)]
            if map_data[start_x][start_y] == " ":
                map_data[start_x][start_y] = "W"  # Placer la première tuile de bois

            while len(wood_tiles) < patch_size:
                tile_x, tile_y = random.choice(wood_tiles)
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Choisir une direction
                new_x = tile_x + direction[0]
                new_y = tile_y + direction[1]

                if 0 <= new_x < size and 0 <= new_y < size:
                    if map_data[new_x][new_y] == " ":  # Placer du bois si la case est d'herbe
                        map_data[new_x][new_y] = "W"
                        wood_tiles.append((new_x, new_y))

    def add_gold_patches(self):
        """Ajoute des paquets d'or (G) sur la carte."""
        num_patches = random.randint(10, 15)  # Nombre de paquets d'or à générer
        min_patch_size = 2  # Taille minimale d'un paquet
        max_patch_size = 5  # Taille maximale d'un paquet

        for _ in range(num_patches):
            patch_size = random.randint(min_patch_size, max_patch_size)
            start_x = random.randint(0, size - 1)
            start_y = random.randint(0, size - 1)

            gold_tiles = [(start_x, start_y)]
            if map_data[start_x][start_y] == " ":
                map_data[start_x][start_y] = "G"  # Placer la première tuile d'or

            while len(gold_tiles) < patch_size:
                tile_x, tile_y = random.choice(gold_tiles)
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # (dx, dy)
                new_x = tile_x + direction[0]
                new_y = tile_y + direction[1]

                if 0 <= new_x < size and 0 <= new_y < size:
                    if map_data[new_x][new_y] == " ":
                        map_data[new_x][new_y] = "G"
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
    
    def add_unit(self, unit, unit_class, quantity, player, unit_tiles):
        """Ajoute une unité dans la carte"""
        for x in range (quantity):
            for y in range(quantity):
                tile_position=Coordinates(unit.position.x+x, unit.position.y+y)

                if tile_position not in unit_tiles:
                    unit_tiles[tile_position] = {}

                if player not in unit_tiles[tile_position]:
                    unit_tiles[tile_position][player] = []

                if not isinstance(unit, Units):
                    return
                
                #création à chaque fois d'une nouvelle instance et l'ajouter dans le dictionnaire tiles
                nunit=unit_class(unit.image,tile_position)
                unit_tiles[tile_position][player].append(nunit)
        
        for position, players in unit_tiles.items():
            for player,units in players.items():
                for unit in units:
                    # vérifier si la position de l'unité et disponible ou pas et l'ajouter si dispo
                    if Coordinates.to_tuple(position)[0] < size and Coordinates.to_tuple(position)[0] < size:
                        if map_data[Coordinates.to_tuple(position)[0]][Coordinates.to_tuple(position)[0]] == " ":
                            map_data[Coordinates.to_tuple(position)[0]][Coordinates.to_tuple(position)[1]] = unit.lettre
                
    def apply_color_filter(self, surface, color):
        """
        Applique un filtre de couleur sur une surface pygame.Surface.
        :param surface: Une surface valide.
        :param color: Tuple (R, G, B) représentant la couleur du filtre.
        :return: Une nouvelle surface avec le filtre appliqué.
        """
        if not isinstance(surface, pygame.Surface):
            raise TypeError("L'objet fourni n'est pas une surface pygame.Surface valide.")

        # Copier la surface d'origine
        image_with_filter = surface.copy()

        # Créer une surface de filtre avec la couleur souhaitée
        color_filter = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)
        color_filter.fill(color)  # Ajouter de la transparence pour le mélange

        # Appliquer le filtre sur l'image
        image_with_filter.blit(color_filter, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        return image_with_filter


    def afficher_buildings(self, grid_x, grid_y, cam_x, cam_y, display_surface):
        tuile = tuiles.get((grid_x, grid_y))
        if not tuile or not tuile.get('batiments'):
            return

        for joueur, buildings in tuile['batiments'].items():
            for tile_type, data in buildings.items():
                if isinstance(data, dict) and data.get('principal'):
                    # Vérifiez si les données du bâtiment existent
                    if tile_type not in builds_dict:
                        return

                    unit_tile = builds_dict.get(tile_type, {}).get('tile')
                    if not unit_tile or not isinstance(unit_tile.image, pygame.Surface):
                        continue  # Si l'image n'est pas valide, passez à l'élément suivant

                    # Récupérer la couleur du joueur depuis PLAYER_COLORS
                    player_color = PLAYER_COLORS.get(joueur, (255, 255, 255))  # Blanc par défaut

                    # Appliquer un filtre de couleur sur une copie de l'image
                    unit_image_colored = self.apply_color_filter(unit_tile.image, player_color)

                    # Calculer les coordonnées cartésiennes de la tuile
                    centered_col = grid_y - size // 2  # Décalage en X (par rapport à la grille)
                    centered_row = grid_x - size // 2  # Décalage en Y (par rapport à la grille)

                    offset_y = tile_grass.height_half - unit_tile.height
                    offset_x = tile_grass.width_half - unit_tile.width

                    # Calcul des coordonnées cartésiennes
                    cart_x = centered_col * tile_grass.width_half
                    cart_y = centered_row * tile_grass.height_half

                    # Conversion en coordonnées isométriques
                    iso_x = (cart_x - cart_y) - cam_x  # - offset_x
                    iso_y = (cart_x + cart_y) / 2 - cam_y + offset_y

                    display_surface.blit(unit_image_colored, (iso_x, iso_y))

    def display_map(self, cam_x, cam_y):
        """Affiche la carte en fonction de la position de la caméra, centrée au milieu."""
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
                        tuiles[(row, col)] = {'ressources': {}}  # Initialiser 'unites' à un dictionnaire vide
                    tuiles[(row, col)]['ressources'] = "W"
                elif tile_type == "G":
                    tile = tile_gold
                    offset_y = tile.height - tile_grass.height
                    if (row, col) not in tuiles:
                        tuiles[(row, col)] = {'ressources': {}}  # Initialiser 'unites' à un dictionnaire vide
                    tuiles[(row, col)]['ressources'] = "G"
                else:
                    tile = tile_grass
                    offset_y = 0

                centered_col = col - half_size
                centered_row = row - half_size 
                cart_x = centered_col * tile_grass.width_half
                cart_y = centered_row * tile_grass.height_half
                iso_x = (cart_x - cart_y) - cam_x
                iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y

                DISPLAYSURF.blit(tile.image, (iso_x, iso_y))

                #self.test_color_filter(display_surface)


    def get_map_data(self):
        #Retourne la carte actuelle pour affichage.
        return map_data
    

