from math import sqrt
import math
from constants import *
from colorama import Fore, Style
from constants import *

class Buildings:
    def __init__(self, image, position, letter, cost, construction_time, hp, size, walkable):
        self.image = image
        self.position = position
        self.letter = letter
        self.cost = cost
        self.construction_time = construction_time
        self.hp = hp
        self.size = size  # tuple (width, height)
        self.walkable = walkable
        
        self.tile_grass = tile_grass
        self.compteurs_joueurs = compteurs_joueurs

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

            for batiment, nombre in data['batiments'].items():
                taille = builds_dict[batiment]['taille']  # Taille du bâtiment (ex. 4 pour un bâtiment 4x4)

                for i in range(nombre):
                    coord_libres = None
                    while coord_libres is None:
                        for offset_x, offset_y in offsets:
                            coord_libres = self.trouver_coordonnees_motif(
                                x, y, taille, tuiles, size, size, offset_x, offset_y
                            )
                            if coord_libres:  # Trouvé une position valide
                                break

                        if not coord_libres:
                                raise ValueError(
                                    f"Impossible de trouver un emplacement libre pour le bâtiment {batiment}."
                                    f"Impossible de trouver un emplacement libre pour le bâtiment {batiment}."
                                )
                    if coord_libres:
                        bat_x, bat_y = coord_libres
                        identifiant = f"{batiment}{i}"
                        self.ajouter_batiment(joueur, batiment, bat_x, bat_y, taille, tuiles, identifiant)

        return tuiles

    


