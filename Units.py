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
            positions.append((cart_y-2, cart_x-2))  # Ajouter les coordonnées à la liste
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
                    if (x, y) not in tuiles or not isinstance(tuiles[(x, y)], dict):
                        tuiles[(x, y)] = {'unites': {}}

                    if not isinstance(tuiles[(x, y)], dict):
                        tuiles[(x, y)] = {'unites': {}}

                    if joueur not in tuiles[(x, y)]['unites']:
                        tuiles[(x, y)]['unites'][joueur] = {}



                    tuile_conflit = ('T' in tuiles[(x, y)]['unites'][joueur]
                                     or 'G' in tuiles[(x, y)]['unites'][joueur]
                                     or 'T' in tuiles[(x, y)]['unites'][joueur]
                                     or 'S' in tuiles[(x, y)]['unites'][joueur]
                                     or 'K' in tuiles[(x, y)]['unites'][joueur]
                                     or 'H' in tuiles[(x, y)]['unites'][joueur]
                                     or 'W' in tuiles[(x, y)]['unites'][joueur]
                                     or 'B' in tuiles[(x, y)]['unites'][joueur])

                    if not tuile_conflit:
                        if unite not in tuiles[(x, y)]['unites'][joueur]:
                            tuiles[(x, y)]['unites'][joueur][unite] = []
                        tuiles[(x, y)]['unites'][joueur][unite].append(identifiant_unite)
                    else:

                        while (x, y) in tuiles and tuile_conflit:
                            x += 1
                            y += 1

                        #print(tuiles[(x, y)]['unites'][joueur])

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

