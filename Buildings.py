from math import sqrt
import math
from constants import *
from colorama import Fore, Style
from constants import *

class Buildings:
    def __init__(self):
        self.tile_grass = tile_grass
        self.map_data = map_data
        self.compteurs_joueurs = compteurs_joueurs

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
                    tuiles[tuile_position] = {'batiments': {}}
                if not isinstance(tuiles[tuile_position], dict):
                    tuiles[tuile_position] = {'batiments': {}}

                if joueur not in tuiles[tuile_position]['batiments']:
                    tuiles[tuile_position]['batiments'][joueur] = {}
                if taille ==4:
                    # Ajouter les informations principales ou secondaires
                    if dx == 3 and dy ==1:  # Nouvelle tuile principale 3-1
                        tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille,
                            'HP': builds_dict[batiment]['hp']
                        }
                    else:  # Tuiles secondaires
                        tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp']
                        }
                elif taille ==3:

                    if dx == 2 and dy ==1:  # Nouvelle tuile principale 2-1
                        tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille,
                            'HP': builds_dict[batiment]['hp']
                        }
                    else:  # Tuiles secondaires
                        tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp']
                        }
                elif taille ==2:

                    if dx == 1 and dy ==0:  # Nouvelle tuile principale 1-0
                        tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille,
                            'HP': builds_dict[batiment]['hp']
                        }
                    else:  # Tuiles secondaires
                        tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp']
                        }
                elif taille == 1:
                    if dx == 0 and dy ==0:  # Nouvelle tuile principale 0-0
                        tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': True,
                            'taille': taille,
                            'HP': builds_dict[batiment]['hp']
                        }
                    else:  # Tuiles secondaires
                        tuiles[tuile_position]['batiments'][joueur][batiment] = {
                            'id': identifiant,
                            'principal': False,
                            'parent': (x, y),
                            'HP': builds_dict[batiment]['hp']
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


