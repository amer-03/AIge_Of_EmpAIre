from math import sqrt
import math
from constants import *
    
def ajouter_unite(self, row, col, unite):
        # Ajoute l'unité si elle n'est pas déjà présente dans la cellule
        map_data[row][col].append(unite)

def afficher_unite(self, tile_type, cart_x, cart_y, cam_x, cam_y, tile_grass, display_surface):
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

        # print("units", cart_x,cart_y)

        # Afficher l'unité
        display_surface.blit(unit_tile.image, (iso_x, iso_y))


def afficher_buildings(self, grid_x, grid_y, cam_x, cam_y, display_surface):
        tuile = tuiles.get((grid_x, grid_y))
        if not tuile or not tuile.get('unites'):
            return

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

                    offset_y = tile_grass.height_half - unit_tile.height
                    offset_x = tile_grass.width_half - unit_tile.width

                    # Calcul des coordonnées cartésiennes
                    cart_x = centered_col * tile_grass.width_half
                    cart_y = centered_row * tile_grass.height_half

                    # Conversion en coordonnées isométriques
                    iso_x = (cart_x - cart_y) - cam_x  # - offset_x
                    iso_y = (cart_x + cart_y) / 2 - cam_y + offset_y

                    display_surface.blit(unit_tile.image, (iso_x, iso_y))


def mode(self, mode):
        if mode == "patches":
            self.add_gold_patches()
        elif mode == "middqle":
            self.add_gold_middle()

def add_wood_patches(self):
        """Ajoute des paquets de bois (W) sur la carte."""
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
                        tuiles[(row, col)] = {'unites': {}}  # Initialiser 'unites' à un dictionnaire vide
                    tuiles[(row, col)]['unites'] = "W"
                elif tile_type == "G":
                    tile = tile_gold
                    offset_y = tile.height - tile_grass.height
                    if (row, col) not in tuiles:
                        tuiles[(row, col)] = {'unites': {}}  # Initialiser 'unites' à un dictionnaire vide
                    tuiles[(row, col)]['unites'] = "G"
                else:
                    tile = tile_grass
                    offset_y = 0

                # Coordonnées cartésiennes centrées
                centered_col = col - half_size  # Décalage en X
                centered_row = row - half_size  # Décalage en Y

                # Conversion en coordonnées isométriques
                cart_x = centered_col * tile_grass.width_half
                cart_y = centered_row * tile_grass.height_half

                iso_x = (cart_x - cart_y) - cam_x
                iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y

                display_surface.blit(tile.image, (iso_x, iso_y))

                if tile_type in ["T", "H", "C", "F", "B", "S", "A", "K"]:
                    self.afficher_buildings(row, col, cam_x, cam_y, display_surface)

                if tile_type in ["v", "s", "h", "a"]:
                    self.afficher_unite(tile_type, cart_x, cart_y, cam_x, cam_y, tile_grass, display_surface)


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

def conversion(self, x, y):
        half_size = map_size // 2  # Assurez-vous que la taille de la carte est correctement définie

        # Décalage centré pour le joueur
        centered_col = y - half_size
        centered_row = x - half_size

        # Conversion en coordonnées isométriques
        cart_x = centered_row * tile_grass.width_half
        cart_y = centered_col * tile_grass.height_half

        iso_x = cart_x - cart_y  # Ne pas soustraire cam_x ici
        iso_y = (cart_x + cart_y) / 2  # Ne pas soustraire cam_y ici

        return iso_x, iso_y

def afficher_unite(self, tile_type, cart_x, cart_y, cam_x, cam_y, tile_grass, display_surface, grid_x, grid_y):
        # Obtenir l'image correspondant au type d'unité

        tuile = tuiles.get((grid_x, grid_y))
        if not tuile or not tuile.get('unites'):
            return

        for joueur, buildings in tuile['unites'].items():

            unit_tile = units_dict.get(tile_type, {}).get('image')
            if not unit_tile:
                return  # Si l'image n'existe pas, ne rien faire

            if not unit_tile or not isinstance(unit_tile.image, pygame.Surface):
                continue  # Si l'image n'est pas valide, passez à l'élément suivant

            # Récupérer la couleur du joueur depuis PLAYER_COLORS
            player_color = PLAYER_COLORS.get(joueur, (255, 255, 255))  # Blanc par défaut

            # Appliquer un filtre de couleur sur une copie de l'image
            unit_image_colored = self.apply_color_filter(unit_tile.image, player_color)

            # Calculer les offsets
            offset_x = tile_grass.width_half - unit_tile.width // 2
            offset_y = tile_grass.height_half - unit_tile.height // 2

            # Recalculer les coordonnées isométriques pour l'unité
            iso_x = (cart_x - cart_y) - cam_x + offset_x
            iso_y = (cart_x + cart_y) / 2 - cam_y - offset_y

            # print("units", cart_x,cart_y)
            display_surface.blit(unit_image_colored, (iso_x, iso_y))

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

def affichage(self):
        for (x, y), tuile in tuiles.items():
            batiments = tuile.get('batiments', {})
            unites = tuile.get('unites', {})
            ressources = tuile.get('ressources', {})

            if not tuile:  # Vérifie si le dictionnaire est vide
                map_data[x][y] = " "
                continue  # Passe à la prochaine tuile


            if isinstance(batiments, dict) or isinstance(unites, dict) or isinstance(ressources, dict):
                if isinstance(unites, dict):
                    for joueur, unites_joueur in unites.items():  # Parcours les unités du joueur
                        if isinstance(unites_joueur, dict):  # Si c'est bien un dictionnaire d'unités
                            for unite, identifiants in unites_joueur.items():  # Parcours chaque type d'unité
                                if unite == 'v':
                                    map_data[x][y] = 'v'
                                    break  # Sortir de la boucle des unités dès qu'une unité est trouvée
                                elif unite == 's':
                                    map_data[x][y] = 's'
                                    break  # Sortir de la boucle des unités dès qu'une unité est trouvée
                                elif unite == 'h':
                                    map_data[x][y] = 'h'
                                    break  # Sortir de la boucle des unités dès qu'une unité est trouvée
                                elif unite == 'a':
                                    map_data[x][y] = 'a'
                                    break  # Sortir de la boucle des unités dès qu'une unité est trouvée
                                else:
                                    map_data[x][y] = " "
                            break
                if map_data[x][y] == " " and isinstance(batiments, dict):
                    for joueur, batiments_joueur in batiments.items():  # Parcours les bâtiments du joueur
                        if isinstance(batiments_joueur, dict):
                            for batiment, details in batiments_joueur.items():
                                if batiment == 'T':  # Vérifier le type de bâtiment
                                    map_data[x][y] = 'T'
                                    break
                                elif batiment == 'H':
                                    map_data[x][y] = 'H'
                                    break
                                elif batiment == 'C':
                                    map_data[x][y] = 'C'
                                    break
                                elif batiment == 'F':
                                    map_data[x][y] = 'F'
                                    break
                                elif batiment == 'B':
                                    map_data[x][y] = 'B'
                                    break
                                elif batiment == 'S':
                                    map_data[x][y] = 'S'
                                    break
                                elif batiment == 'A':
                                    map_data[x][y] = 'A'
                                    break
                                elif batiment == 'K':
                                    map_data[x][y] = 'K'
                                    break
                                else:
                                    map_data[x][y] = " "
                            break

                # Vérification et affichage des ressources (on passe par ressources si elles existent)
                if map_data[x][y] == " " and isinstance(ressources, dict):
                    for joueur, ressources_joueur in ressources.items():  # Parcours les ressources du joueur
                        if isinstance(ressources_joueur, dict):
                            for ressource, details in ressources_joueur.items():
                                if ressource == 'G':
                                    map_data[x][y] = 'G'
                                elif ressource == 'W':
                                    map_data[x][y] = 'W'
                                else:
                                    map_data[x][y] = " "

        for i in range(len(map_data)):
            for j in range(len(map_data[i])):
                if (i, j) not in tuiles:
                    map_data[i][j] = " "  # Case vide par défaut

def conversion(self, x, y):
        half_size = size // 2  # Assurez-vous que la taille de la carte est correctement définie

        # Décalage centré pour le joueur
        centered_col = y - half_size
        centered_row = x - half_size

        # Conversion en coordonnées isométriques
        cart_x = centered_row * tile_grass.width_half
        cart_y = centered_col * tile_grass.height_half

        iso_x = cart_x - cart_y  # Ne pas soustraire cam_x ici
        iso_y = (cart_x + cart_y) / 2  # Ne pas soustraire cam_y ici

        return iso_x, iso_y

def decrementer_hp_batiments(self):
        """Décroît les HP des bâtiments dans le dictionnaire tuiles, en tenant compte des bâtiments multi-tuiles."""
        traites = set()  # Pour éviter de traiter plusieurs fois le même bâtiment

        for (x, y), data in list(tuiles.items()):
            if isinstance(data, dict) and 'batiments' in data:
                batiments = data['batiments']

                for joueur, joueur_batiments in list(batiments.items()):
                    for unite, stats in list(joueur_batiments.items()):
                        if isinstance(stats, dict):
                            # Identifier la tuile principale
                            parent = stats.get('parent', (x, y))
                            identifiant = stats.get('id', 'Inconnu')

                            # Si déjà traité, passer
                            if (joueur, identifiant) in traites:
                                continue

                            # Ajouter à la liste des traités
                            traites.add((joueur, identifiant))

                            if 'HP' in stats:
                                stats['HP'] -= 250

                                # Si les HP tombent à 0, supprimer le bâtiment
                                if stats['HP'] <= 0:
                                    stats['HP'] = 0
                                    self.supprimer_batiment(tuiles, joueur, identifiant, parent)
                                    if joueur in compteurs_joueurs:
                                        if unite in compteurs_joueurs[joueur]['batiments'] and \
                                                compteurs_joueurs[joueur]['batiments'][unite] > 0:
                                            compteurs_joueurs[joueur]['batiments'][unite] -= 1
                                return

def supprimer_batiment(self,tuiles, joueur, identifiant, parent):
        """Supprime un bâtiment multi-tuiles."""
        tuiles_a_supprimer = []



        for (x, y), data in list(tuiles.items()):
            if 'batiments' in data and joueur in data['batiments']:
                batiments = data['batiments'][joueur]

                for unite, stats in list(batiments.items()):
                    if isinstance(stats, dict) and stats.get('id') == identifiant:
                        del tuiles[(x, y)]['batiments'][joueur][unite]



                        # Si le niveau est vide, marquer pour suppression
                        if not tuiles[(x, y)]['batiments'][joueur]:
                            del tuiles[(x, y)]['batiments'][joueur]
                        if not tuiles[(x, y)]['batiments']:
                            tuiles_a_supprimer.append((x, y))

        # Supprimer les tuiles marquées
        for tuile in tuiles_a_supprimer:
            del tuiles[tuile]