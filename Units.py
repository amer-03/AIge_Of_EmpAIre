from math import sqrt
import math
import pygame
from constants import *
import random

from constants import map_size


class Unit:
    def __init__(self):
        self.map_size = map_size
        self.tile_grass = tile_grass
        self.map_data = map_data
        self.compteurs_joueurs = compteurs_joueurs

    def conversion(self, x, y):
        half_size = map_size//2  # Assurez-vous que la taille de la carte est correctement définie

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



    #pour del : del tuiles[(60, 110)]['unites']['v'][0]


    def initialisation_compteur(self,position):

        for idx, (joueur, data) in enumerate(compteurs_joueurs.items()):
            x, y = position[idx]  # Position initiale de chaque joueur


            for unite, nombre in data['unites'].items():
                compteurs_unites[unite] = 0

                for i in range(nombre):
                    identifiant_unite = compteurs_unites[unite]
                    compteurs_unites[unite] += 1
                    if (x, y) not in tuiles:
                        tuiles[(x, y)] = {'unites': {}}

                    if joueur not in tuiles[(x, y)]['unites']:
                        tuiles[(x, y)]['unites'][joueur] = {}

                    tuile_conflit = ('T' in tuiles[(x, y)]['unites'][joueur]
                                     or 'G' in tuiles[(x, y)]['unites'][joueur]
                                     or 'W' in tuiles[(x, y)]['unites'][joueur])

                    if not tuile_conflit:
                        if unite not in tuiles[(x, y)]['unites'][joueur]:
                            tuiles[(x, y)]['unites'][joueur][unite] = []
                        tuiles[(x, y)]['unites'][joueur][unite].append(identifiant_unite)
                    else:

                        while (x, y) in tuiles and (
                                'G' in tuiles[(x, y)]['unites'][joueur] or
                                'W' in tuiles[(x, y)]['unites'][joueur] or
                                'T' in tuiles[(x, y)]['unites'][joueur]
                        ):
                            x += 1
                            y += 1

                        if (x, y) not in tuiles:
                            tuiles[(x, y)] = {'unites': {}}

                        if joueur not in tuiles[(x, y)]['unites']:
                            tuiles[(x, y)]['unites'][joueur] = {}

                        if unite not in tuiles[(x, y)]['unites'][joueur]:
                            tuiles[(x, y)]['unites'][joueur][unite] = []
                        tuiles[(x, y)]['unites'][joueur][unite].append(identifiant_unite)







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



    """
    def affichage(self, n):
        # Placer les joueurs sur un cercle

        positions_joueurs = self.placer_joueurs_cercle(n, 50, map_size // 2, map_size // 2)
        #print (compteurs_joueurs)

        for idx, (joueur, data) in enumerate(compteurs_joueurs.items()):
            x, y = positions_joueurs[idx]
            print(x,y)


            # Afficher les unités pour ce joueur
            for unite, nombre in data['unites'].items():
                if nombre > 0:
                    print(f"Nombre d'unités de type {unite}: {nombre}")

                    # Placer le premier exemplaire d'unité à la position de départ (x, y)
                    if map_data[x][y] == " ":
                        map_data[x][y] = unite
                        print(f"Placé {unite} à la position de départ ({x}, {y})")

                    # Placer les unités restantes en utilisant une expansion en spirale
                    placed_count = 1  # On commence avec une unité placée
                    radius = 1  # Rayon d'expansion à chaque étape de la spirale

                    while placed_count < nombre:
                        # Parcourir les positions dans le rayon actuel autour de (x, y)
                        for dx in range(-radius, radius + 1):
                            for dy in range(-radius, radius + 1):
                                # Calculer la nouvelle position
                                new_x, new_y = x + dx, y + dy

                                # Vérifier que la position est dans les limites et vide
                                if (0 <= new_x < len(map_data) and 0 <= new_y < len(map_data[0]) and
                                        map_data[new_x][new_y] == " "):
                                    map_data[new_x][new_y] = unite  # Placer l'unité
                                    print(f"Placé {unite} à ({new_x}, {new_y})")
                                    placed_count += 1  # Incrémenter le compteur d'unités placées

                                    if placed_count >= nombre:
                                        break  # Sortir si toutes les unités sont placées
                            if placed_count >= nombre:
                                break  # Sortir si toutes les unités sont placées
                        radius += 1

    """



"""
class Villager(Unit):
    def __init__(self):
        super().__init__(cost_food=50, cost_gold=0, training_time=25, hp=25, attack=1, speed=0.8)
        self.image = swordsman_image

class Swordsman(Unit):
    def __init__(self):
        super().__init__(cost_food=50, cost_gold=20, training_time=20, hp=40, attack=4, speed=0.9)


class Horseman(Unit):
    def __init__(self):
        super().__init__(cost_food=80, cost_gold=20, training_time=30, hp=45, attack=4, speed=1.2)


class Archer(Unit):
    def __init__(self):
        super().__init__(cost_food=25, cost_gold=45, training_time=35, hp=30, attack=4, speed=1.0, range_=4)
"""