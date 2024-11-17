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
            positions.append((cart_y, cart_x))  # Ajouter les coordonnées à la liste
        return positions

    # pour del : del tuiles[(60, 110)]['unites']['v'][0]

    def initialisation_compteur(self, position):
        print("test", position)
        print("compteuur", compteurs_joueurs)

        for idx, (joueur, data) in enumerate(compteurs_joueurs.items()):
            x, y = position[idx]  # Position initiale pour ce joueur

            for batiment, nombre in data['batiments'].items():
                taille = builds_images[batiment]['taille']  # Taille du bâtiment (NxN)

                for i in range(nombre):

                    # Trouver un espace disponible pour le bâtiment
                    espace_libre = False
                    while not espace_libre:
                        espace_libre = True
                        for dx in range(taille):
                            for dy in range(taille):

                                # Vérifie si une des tuiles nécessaires est occupée
                                if (x + dx, y + dy) in tuiles and tuiles[(x + dx, y + dy)]['unites']:
                                    print(x + dx, y + dy)
                                    espace_libre = False
                                    break
                            if not espace_libre:
                                break
                        if not espace_libre:
                            x += 1  # Incrémenter pour chercher une nouvelle position
                            y += 1

                    # Réserver l'espace pour le bâtiment et l'associer au joueur
                    for dx in range(taille):
                        for dy in range(taille):
                            print(x + dx, y + dy)
                            tuile_position = (x + dx, y + dy)
                            if tuile_position not in tuiles:
                                tuiles[tuile_position] = {'unites': {}}

                            # Ajouter le bâtiment et associer le joueur sous la clé du joueur
                            if joueur not in tuiles[tuile_position]['unites']:
                                tuiles[tuile_position]['unites'][joueur] = {}

                            if dx == 3 and dy == 1:  # La tuile principale (coin supérieur gauche)
                                tuiles[tuile_position]['unites'][joueur][batiment] = {
                                    'id': f"{batiment}{i}",  # Identifiant unique
                                    'principal': True,  # Marquer comme principale
                                    'taille': taille  # Stocker la taille
                                }
                            else:  # Tuiles secondaires
                                tuiles[tuile_position]['unites'][joueur][batiment] = {
                                    'id': f"{batiment}{i}",
                                    'principal': False,  # Marquer comme secondaire
                                    'parent': (x, y)  # Référence vers la tuile principale
                                }

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
                        if 'T' in unites_joueur:
                            map_data[x][y] = 'T'
                        elif 'H' in unites_joueur:
                            map_data[x][y] = 'H'
                        elif 'G' in unites_joueur:
                            map_data[x][y] = 'G'
                        elif 'W' in unites_joueur:
                            map_data[x][y] = 'W'
