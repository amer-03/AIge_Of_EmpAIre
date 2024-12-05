from math import sqrt
import math
import pygame
from constants import *
import random
from constants import map_size, tile_grass, map_data, compteurs_joueurs, tuiles, compteurs_unites

class Unit:
    def __init__(self, type=None, tile_x=0, tile_y=0, player=None):  # Ajout des paramètres par défaut
        self.map_size = map_size
        self.tile_grass = tile_grass
        self.map_data = map_data
        self.compteurs_joueurs = compteurs_joueurs
        self.target_x = None
        self.target_y = None
        self.is_moving = False
        self.type = type
        self.player = player
        self.tile_x = tile_x  
        self.tile_y = tile_y  
        self.speed = 1   

    def initialiser_villageois(self, id_villageois, player, tile_x, tile_y):
        """Initialise un nouveau villageois à des coordonnées spécifiques et l'ajoute au dictionnaire des tuiles."""
        villageois = {
            'id': id_villageois,
            'x': tile_x,
            'y': tile_y,
            'type': 'v'
        }
        self.player = player
        self.type = 'v'
        self.ajouter_dans_tuile(villageois)
        self.affichage()
        self.player = player

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


    def ajouter_dans_tuile(self, villageois):
        """Ajoute le villageois dans le dictionnaire des tuiles."""
        try:
            tile_key = (villageois['x'], villageois['y'])
            if tile_key not in tuiles:
                tuiles[tile_key] = {'unites': {}}
            if self.player is None:
                raise ValueError("Player non défini")
            if 'unites' not in tuiles[tile_key]:
                tuiles[tile_key]['unites'] = {}
            if self.player not in tuiles[tile_key]['unites']:
                tuiles[tile_key]['unites'][self.player] = {}
            if 'v' not in tuiles[tile_key]['unites'][self.player]:
                tuiles[tile_key]['unites'][self.player]['v'] = []
            tuiles[tile_key]['unites'][self.player]['v'].append(villageois['id'])
        except Exception as e:
            print(f"Erreur lors de l'ajout dans la tuile: {str(e)}")

    def afficher_sur_carte(self, villageois):
        """Affiche le villageois sur la carte."""
        iso_x, iso_y = self.conversion(villageois['x'], villageois['y'])
        # Code pour afficher le villageois sur la carte en utilisant iso_x et iso_y
        print(f"Villageois {villageois['id']} affiché à ({iso_x}, {iso_y}) sur la carte.")

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



    def target(self, target_x, target_y):
        if ((self.map_data[int(self.tile_y)][int(self.tile_x)] == " ") or 
            (self.map_data[int(self.tile_y)][int(self.tile_x)] == "G") or 
            (self.map_data[int(self.tile_y)][int(self.tile_x)] == "W")):
            self.target_x = target_x
            self.target_y = target_y
            self.is_moving = True

    def update_position(self):
        try:
            if self.is_moving and self.target_x is not None and self.target_y is not None:
                dx = self.target_x - self.tile_x
                dy = self.target_y - self.tile_y
                distance = sqrt(dx**2 + dy**2)

                if distance > 0.05:
                    self.tile_x += (dx / distance) * self.speed
                    self.tile_y += (dy / distance) * self.speed
                else:
                    self.tile_x = self.target_x
                    self.tile_y = self.target_y
                    self.is_moving = False
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la position: {str(e)}")
            self.is_moving = False

    def affichage(self):
        try:
            for (x, y), tuile in tuiles.items():
                if not isinstance(tuile, dict) or 'unites' not in tuile:
                    continue
                
                if 0 <= x < len(self.map_data) and 0 <= y < len(self.map_data[0]):
                    for joueur, unites_joueur in tuile['unites'].items():
                        if not isinstance(unites_joueur, dict):
                            continue
                            
                        for unite, identifiant in unites_joueur.items():
                            if unite in ['v', 's', 'h', 'a', 'C', 'F', 'B', 'S', 'A', 'K', 'T', 'H', 'G', 'W']:
                                self.map_data[x][y] = unite
        except Exception as e:
            print(f"Erreur lors de l'affichage: {str(e)}")



