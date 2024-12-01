from math import sqrt
import math
import pygame
from constants import *

from constants import map_size

class Buildings:
    def __init__(self):
        self.map_size = map_size
        self.tile_grass = tile_grass
        self.map_data = map_data
        self.compteurs_joueurs = compteurs_joueurs

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

    def placer_joueurs_cercle(self, players, rayon, center_x, center_y):
        """Calcule les positions cartésiennes pour `n` joueurs répartis en cercle autour du centre."""
        positions = []
        angle_increment = 360 / players  # Divise le cercle en n parties égales
        for i in range(players):
            angle = angle_increment * i
            cart_x = int(center_x + rayon * math.cos(math.radians(angle)))  # Calcul de la position X
            cart_y = int(center_y + rayon * math.sin(math.radians(angle)))  # Calcul de la position Y
            positions.append((cart_y-2, cart_x-2))  # Ajouter les coordonnées à la liste
        return positions

    # pour del : del tuiles[(60, 110)]['unites']['v'][0]

    def trouver_coordonnees_motif(self, x, y, taille, tuiles, max_x, max_y, offset_x, offset_y):
        start_x = x + offset_x * taille
        start_y = y + offset_y * taille

        # Vérification si les coordonnées sont dans les limites de la grille
        if 0 <= start_x < max_x and 0 <= start_y < max_y:
            # Vérification de l'espace libre pour le bâtiment
            espace_libre = True
            for dx in range(taille):
                for dy in range(taille):
                    tuile_position = (start_x + dx, start_y + dy)
                    if tuile_position in tuiles :  # Vérifie si la position est déjà occupée
                        #print(f"Tuile occupée détectée : {tuile_position}")
                        espace_libre = False
                        break
                if not espace_libre:
                    break

            # Si l'espace est libre, retourne les coordonnées
            if espace_libre:
                # Marquer toutes les tuiles comme occupées
                for dx in range(taille):
                    for dy in range(taille):
                        tuile_position = (start_x + dx, start_y + dy)
                        tuiles[tuile_position] = "occupé"  # Marquer la tuile comme occupée
                #print(start_x, start_y)
                return start_x, start_y

        return None


    def ajouter_batiment(self,joueur, batiment, x, y, taille, tuiles, identifiant):
            # Si toutes les tuiles sont libres, les réserver et placer le bâtiment
        for dx in range(taille):
            for dy in range(taille):
                tuile_position = (x + dx, y + dy)

                # Initialiser la tuile si nécessaire
                if tuile_position not in tuiles:
                    tuiles[tuile_position] = {'unites': {}}
                if not isinstance(tuiles[tuile_position], dict):
                    tuiles[tuile_position] = {'unites': {}}

                if joueur not in tuiles[tuile_position]['unites']:
                    tuiles[tuile_position]['unites'][joueur] = {}
                if taille ==4:
                    # Ajouter les informations principales ou secondaires
                    if dx == 3 and dy ==1:  # Nouvelle tuile principale 3-1
                        tuiles[tuile_position]['unites'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille
                        }
                    else:  # Tuiles secondaires
                        tuiles[tuile_position]['unites'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y)
                        }
                elif taille ==3:

                    if dx == 2 and dy ==1:  # Nouvelle tuile principale 2-1
                        tuiles[tuile_position]['unites'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille
                        }
                    else:  # Tuiles secondaires
                        tuiles[tuile_position]['unites'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y)
                        }
                elif taille ==2:

                    if dx == 1 and dy ==0:  # Nouvelle tuile principale 1-0
                        tuiles[tuile_position]['unites'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille
                        }
                    else:  # Tuiles secondaires
                        tuiles[tuile_position]['unites'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y)
                        }
                elif taille == 1:
                    if dx == 0 and dy ==0:  # Nouvelle tuile principale 0-0
                        tuiles[tuile_position]['unites'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille
                        }
                    else:  # Tuiles secondaires
                        tuiles[tuile_position]['unites'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y)
                        }

    def generer_offsets(self):
        for joueur, compteurs in compteurs_joueurs.items():
            if sum(compteurs['batiments'].values())<=9:
                portee = 2
            elif sum(compteurs['batiments'].values())<=25:
                portee = 3
            elif sum(compteurs['batiments'].values()) <= 49:
                portee = 4
            else :
                portee =5

            offsets = [(dx, dy) for dx in range(-portee, portee + 1) for dy in range(-portee, portee + 1)]
            # Trier d'abord par distance Manhattan, puis par proximité radiale
            return sorted(offsets, key=lambda offset: (abs(offset[0]) + abs(offset[1]), abs(offset[0]), abs(offset[1])))
        #return offsets

    def initialisation_compteur(self, position):


        for idx, (joueur, data) in enumerate(compteurs_joueurs.items()):
            x, y = position[idx]  # Point central pour ce joueur
            offsets = self.generer_offsets()
            #print(f"Offsets générés : {offsets}")

            for batiment, nombre in data['batiments'].items():
                taille = builds_images[batiment]['taille']  # Taille du bâtiment (ex. 4 pour un bâtiment 4x4)

                for i in range(nombre):
                    coord_libres = None
                    while coord_libres is None:
                        for offset_x, offset_y in offsets:
                            #print("offset", offset_x, offset_y)
                            #print("x, y", x,y)
                            #print("taille", taille)
                            coord_libres = self.trouver_coordonnees_motif(
                                x, y, taille, tuiles, size, size, offset_x, offset_y
                            )
                            if coord_libres:  # Trouvé une position valide
                                break

                        if not coord_libres:
                                raise ValueError(
                                    f"Impossible de trouver un emplacement libre pour le bâtiment {batiment}."
                                )
                    if coord_libres:
                        bat_x, bat_y = coord_libres
                        identifiant = f"{batiment}{i}"
                        print(f"Bâtiment {batiment} placé en {coord_libres} avec taille {taille}")
                        self.ajouter_batiment(joueur, batiment, bat_x, bat_y, taille, tuiles, identifiant)
                        #print("ok")
                        #print(tuiles)

        return tuiles



    def affichage(self):

        for (x, y), tuile in tuiles.items():

            if isinstance(tuile['unites'], dict):  # Vérifie que 'unites' est un dictionnaire
                for joueur, unites_joueur in tuile['unites'].items():

                    if isinstance(unites_joueur, dict):  # Vérifie que c'est bien un joueur avec des unités
                        # Parcourir les unités de ce joueur et les afficher
                        for unite, identifiant in unites_joueur.items():
                            # Afficher selon le type d'unité/bâtiment
                            if unite == 'v':
                                map_data[x][y] = 'v'
                            elif unite == 's':
                                map_data[x][y] = 's'
                            elif unite == 'h':
                                map_data[x][y] = 'h'
                            elif unite == 'a':
                                map_data[x][y] = 'a'

                            elif  unite =='T':
                                map_data[x][y] = 'T'
                            elif unite =='H':
                                map_data[x][y] = 'H'
                            elif unite == 'C':
                                map_data[x][y] = 'C'
                            elif unite == 'F':
                                map_data[x][y] = 'F'
                            elif unite == 'B':
                                map_data[x][y] = 'B'
                            elif unite == 'S':
                                map_data[x][y] = 'S'
                            elif unite == 'A':
                                map_data[x][y] = 'A'
                            elif unite == 'K':
                                map_data[x][y] = 'K'

                        # Gestion des bâtiments
                        # Vérifier si l'unité est un bâtiment comme 'T' et l'afficher

                        if 'G' in unites_joueur:
                            map_data[x][y] = 'G'
                        elif 'W' in unites_joueur:
                            map_data[x][y] = 'W'
