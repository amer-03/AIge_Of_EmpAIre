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
        self.unit_list = None
        self.current_unit_index = 0

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

    def initialisation_compteur(self, position):
        for idx, (joueur, data) in enumerate(compteurs_joueurs.items()):
            x, y = position[idx]  # Position initiale de chaque joueur

            for unite, nombre in data['unites'].items():
                compteurs_unites[unite] = 0

                for i in range(nombre):
                    identifiant_unite = compteurs_unites[unite]
                    compteurs_unites[unite] += 1

                    # Si la tuile (x, y) n'existe pas ou n'est pas un dictionnaire, l'initialiser
                    if (x, y) not in tuiles or not isinstance(tuiles[(x, y)], dict):
                        tuiles[(x, y)] = {}

                    # Si la clé 'unites' n'existe pas, l'ajouter
                    if 'unites' not in tuiles[(x, y)]:
                        tuiles[(x, y)]['unites'] = {}

                    # Si le joueur n'est pas dans 'unites', l'ajouter
                    if joueur not in tuiles[(x, y)]['unites']:
                        tuiles[(x, y)]['unites'][joueur] = {}

                    # Vérifier s'il y a un conflit avec les bâtiments ou ressources
                    batiments = tuiles[(x, y)].get('batiments', {})
                    ressources = tuiles[(x, y)].get('ressources', {})

                    # Vérifier s'il y a des bâtiments ou des ressources sur la tuile
                    tuile_conflit = ('W' in ressources.get(joueur, {}) or
                                     'G' in ressources.get(joueur, {}) or
                                     'T' in batiments.get(joueur, {}) or
                                     'S' in batiments.get(joueur, {}) or
                                     'K' in batiments.get(joueur, {}) or
                                     'H' in batiments.get(joueur, {}) or
                                     'B' in batiments.get(joueur, {}))

                    # Ajouter l'unité seulement s'il n'y a pas de conflit
                    if not tuile_conflit:
                        if unite not in tuiles[(x, y)]['unites'][joueur]:
                            tuiles[(x, y)]['unites'][joueur][unite] = {}

                        tuiles[(x, y)]['unites'][joueur][unite][identifiant_unite] = {
                            'HP': units_dict[unite]['hp']  # Récupérer les HP depuis units_images
                        }
                    else:
                        # Si conflit, trouver une autre position et réessayer
                        while (x, y) in tuiles and tuile_conflit:
                            x += 1
                            y += 1

                        # Réinitialiser la tuile (x, y) avec les clés nécessaires
                        if (x, y) not in tuiles:
                            tuiles[(x, y)] = {'unites': {}}

                        if joueur not in tuiles[(x, y)]['unites']:
                            tuiles[(x, y)]['unites'][joueur] = {}

                        if unite not in tuiles[(x, y)]['unites'][joueur]:
                            tuiles[(x, y)]['unites'][joueur][unite] = {}

                        tuiles[(x, y)]['unites'][joueur][unite][identifiant_unite] = {
                            'HP': units_dict[unite]['hp']  # Récupérer les HP depuis units_images
                        }

    def decrementer_hp_unite(self):
        """Décroit les HP de la première unité rencontrée dans le dictionnaire tuiles."""
        # Vérifier que les tuiles existent et contiennent des unités
        for (x, y), data in tuiles.items():
            if isinstance(data, dict) and 'unites' in data:  # Vérifie si la tuile contient des unités
                unites = data['unites']

                # Parcourir les joueurs
                for joueur, joueur_unites in unites.items():
                    # Parcourir les types d'unités
                    for unite, instances in joueur_unites.items():
                        # Prendre uniquement la première unité trouvée
                        for identifiant, stats in instances.items():
                            if 'HP' in stats:
                                stats['HP'] -= 4  # Réduire les HP de 4
                                print(f"Unité {unite} (ID: {identifiant}) à ({x},{y}) a maintenant {stats['HP']} HP.")

                                # Si l'unité est morte, la supprimer
                                if stats['HP'] <= 0:
                                    stats['HP'] = 0
                                    print(f"L'unité {unite} (ID: {identifiant}) est morte.")
                                    del tuiles[(x, y)]['unites'][joueur][unite][identifiant]

                                    # Supprimer les structures vides
                                    if not tuiles[(x, y)]['unites'][joueur][unite]:
                                        del tuiles[(x, y)]['unites'][joueur][unite]
                                    if not tuiles[(x, y)]['unites'][joueur]:
                                        del tuiles[(x, y)]['unites'][joueur]
                                    if not tuiles[(x, y)]['unites']:
                                        del tuiles[(x, y)]['unites']
                                return






