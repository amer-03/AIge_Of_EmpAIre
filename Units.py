from math import sqrt
import math
import pygame
from TileMap import *
from constants import *
from Coordinates import *
import random
import time

from pygame.mixer_music import queue


class Unit:
    def __init__(self):
        self.tile_grass = tile_grass
        self.map_data = map_data  # Dictionnaire global à modifier
        self.compteurs_joueurs = compteurs_joueurs
        self.unit_list = None
        self.current_unit_index = 0

        self.tile_map = TileMap()
        self.coordinates = Coordinates()


        self.id = None  # Identifiant unique pour l'unité

        #self.position = (60, 60)  # Position initiale de l'unité (60, 60)
        self.target_position = None
        self.moving = False
        self.move_start_time = 0
        self.move_duration = 0
        self.frame_index = 0
        self.direction_index = 0
        self.last_time = pygame.time.get_ticks()

    def deplacer_unite(self, joueur, type_unite, id_unite, nouvelle_position):
        """
        Déplace une unité d'une position à une autre dans map_data.

        :param joueur: Nom du joueur (ex. 'joueur_1').
        :param type_unite: Type de l'unité (ex. 'v', 'a', 's', etc.).
        :param id_unite: Identifiant unique de l'unité à déplacer.
        :param nouvelle_position: Nouvelle position (x, y) de l'unité.
        """
        # Rechercher l'unité dans map_data
        position_actuelle = None
        for position, data in tuiles.items():
            if 'unites' in data and joueur in data['unites'] and type_unite in data['unites'][joueur]:
                if id_unite in data['unites'][joueur][type_unite]:

                    position_actuelle = position
                    break

        if not position_actuelle:
            print(f"Unité {id_unite} non trouvée pour le joueur {joueur}.")
            return

        # Récupérer les données de l'unité
        unite_data = tuiles[position_actuelle]['unites'][joueur][type_unite].pop(id_unite)

        # Si aucune autre unité n'existe à cette position, nettoyez les entrées inutiles
        if not tuiles[position_actuelle]['unites'][joueur][type_unite]:
            del tuiles[position_actuelle]['unites'][joueur][type_unite]
        if not tuiles[position_actuelle]['unites'][joueur]:
            del tuiles[position_actuelle]['unites'][joueur]
        if position_actuelle in tuiles:
            if 'unites' in tuiles[position_actuelle]:
                del tuiles[position_actuelle]['unites']
            if not tuiles[position_actuelle]:  # Si la tuile est vide, la supprimer
                del tuiles[position_actuelle]

        # Ajouter l'unité à la nouvelle position
        if nouvelle_position not in tuiles:
            tuiles[nouvelle_position] = {'unites': {}}
        if 'unites' not in tuiles[nouvelle_position]:
            tuiles[nouvelle_position]['unites'] = {}
        if joueur not in tuiles[nouvelle_position]['unites']:
            tuiles[nouvelle_position]['unites'][joueur] = {}
        if type_unite not in tuiles[nouvelle_position]['unites'][joueur]:
            tuiles[nouvelle_position]['unites'][joueur][type_unite] = {}

        tuiles[nouvelle_position]['unites'][joueur][type_unite][id_unite] = unite_data

        # Mettre à jour la position de l'unité dans votre instance
        self.start_moving(nouvelle_position[0], nouvelle_position[1])

        print(f"Unité {id_unite} déplacée de {position_actuelle} à {nouvelle_position}.")

    def start_moving(self, new_x, new_y, duration=1000):
        """Démarre l'animation de déplacement de l'unité."""
        self.target_position = (new_x, new_y)
        self.move_start_time = pygame.time.get_ticks()
        self.move_duration = duration
        self.moving = True
        print(f"Déplacement vers la position: {new_x}, {new_y}")

    def update_position(self, start_x, start_y):
        """Met à jour la position de l'unité pendant le mouvement."""
        if not self.moving:
            return

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.move_start_time

        # Si le mouvement est terminé, on arrête l'animation
        if elapsed_time >= self.move_duration:
            self.position = self.target_position
            self.moving = False
            print(f"Arrivée à la position: {self.position}")
            return

        # Sinon, on calcule la position intermédiaire en fonction du temps écoulé
        progress = elapsed_time / self.move_duration
        #start_x, start_y = self.position
        target_x, target_y = self.target_position

        # L'animation fait progresser l'unité entre sa position actuelle et la cible
        new_x = start_x + (target_x - start_x) * progress
        new_y = start_y + (target_y - start_y) * progress
        self.position = (new_x, new_y)
        self.animation(current_time)

    def animation(self, current_time):  # fonction qui modifie l'indice des frames et le dernier temps du frame
        if current_time - self.last_time > 1000 // 30:  # 1000//30: 30 frames par 1000 millisecondes
            self.last_time = current_time
            self.frame_index = (self.frame_index + 1) % 30

    def frame_coordinates(self, unit_image):
        # calcul des tailles du chaque frame en divisant la taille de l'image principal par le nombre des frames
        frame_width = unit_image.get_width() // 30  # 30 nombre des frames par lignes
        frame_height = unit_image.get_height() // 16  # 16 nombre des frames par colonnes

        # multiplication de l'indice du frame par la taille de chaque frame pour chercher les vrai coordonnees
        frame_x = self.frame_index * frame_width
        frame_y = self.direction_index * frame_height

        return frame_x, frame_y, frame_width, frame_height


    def diplay_unit(self,position_x, position_y, cam_x, cam_y, current_time, unit_image):
        # coordonnées isométrique
        self.update_position(position_x,position_y)
        iso_x, iso_y = self.coordinates.to_iso(position_x, position_y, cam_x, cam_y)

        # appel de la fonction de l'animation
        self.animation(current_time)

        # appel de la fonction frame_coordinates
        frame_x, frame_y, frame_width, frame_height = self.frame_coordinates(unit_image)

        # enlever un frame de l'image principal et l'afficher a la fois
        #frame_rect = pygame.Rect(frame_x, frame_y, frame_width, frame_height)
        #unit_frame = unit_image.subsurface(frame_rect)

        #DISPLAYSURF.blit(unit_frame, (iso_x, iso_y))

    def conversion(self, x, y):

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

                    if not isinstance(ressources, dict):
                        ressources = {}
                    if not isinstance(batiments, dict):
                        batiments = {}

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
                            'HP': units_dict[unite]['hp'],  # Récupérer les HP depuis units_images
                            'Status': 'libre',
                            'capacite': '0'
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
                            'HP': units_dict[unite]['hp'],  # Récupérer les HP depuis units_images
                            'Status': 'libre',
                            'capacite': '0'
                        }

                        #tuiles[(x, y)]['unites'][joueur][unite][identifiant_unite] = {
                        #    'occupé': False  # Récupérer les HP depuis units_images
                        #}

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

                                # Si l'unité est morte, la supprimer
                                if stats['HP'] <= 0:
                                    stats['HP'] = 0
                                    del tuiles[(x, y)]['unites'][joueur][unite][identifiant]
                                    if joueur in compteurs_joueurs:
                                        if unite in compteurs_joueurs[joueur]['unites'] and \
                                                compteurs_joueurs[joueur]['unites'][unite] > 0:
                                            compteurs_joueurs[joueur]['unites'][unite] -= 1


                                    # Supprimer les structures vides
                                    if not tuiles[(x, y)]['unites'][joueur][unite]:
                                        del tuiles[(x, y)]['unites'][joueur][unite]
                                    if not tuiles[(x, y)]['unites'][joueur]:
                                        del tuiles[(x, y)]['unites'][joueur]
                                    if not tuiles[(x, y)]['unites']:
                                        del tuiles[(x, y)]['unites']
                                return



    def creation_unite(self, unit_type, player):
        """ Il faudra modifier plus tard afin de pouvoir choisir le batiment spécifique du joueur en fonction d'ou il veut créer ses unités"""
        # Définir le type de bâtiment nécessaire pour chaque unité
        required_buildings = {"v": "T", "a": "A", "h": "H", "s": "S"}
        building_type = required_buildings.get(unit_type)

        required_cost = units_dict[unit_type]['cout']
        if (compteurs_joueurs[player]["ressources"]['W'] >= required_cost['W']
                and compteurs_joueurs[player]["ressources"]['G'] >= required_cost['G']
                and compteurs_joueurs[player]["ressources"]['F'] >= required_cost['F']):
            if not building_type:
                return
            if compteurs_joueurs[player]['ressources']['U'] < compteurs_joueurs[player]['ressources']['max_pop']:

                # Rechercher les bâtiments valides pour le joueur
                for (x, y), tile in tuiles.items():
                    if "batiments" in tile and player in tile["batiments"]:
                        if building_type in tile["batiments"][player]:
                            # Ajouter à la file d'attente de ce bâtiment
                            compteurs_joueurs[player]["ressources"]['W'] -= required_cost['W']
                            compteurs_joueurs[player]["ressources"]['F'] -= required_cost['F']
                            compteurs_joueurs[player]["ressources"]['G'] -= required_cost['G']
                            if player in compteurs_joueurs:
                                if unit_type in compteurs_joueurs[player]['unites']:
                                    compteurs_joueurs[player]['unites'][unit_type] += 1
                                    compteurs_joueurs[player]['ressources']['U'] += 1
                                    print("incrémentation compteur", compteurs_joueurs[player]['ressources']['U'])
                            self.add_unit_to_queue(unit_type, player, (x, y))

                            return
            else :
                print("nombre max d'unité atteint")
            print("pas assez de ressources")

    def is_tile_empty(self, position):
        tile = tuiles.get(position, {})
        return "batiments" not in tile and "ressources" not in tile

    def add_unit_to_tile(self, unit_type, player, position):

        if position not in tuiles:
            tuiles[position] = {}

        if "unites" not in tuiles[position]:
            tuiles[position]["unites"] = {}

        if player not in tuiles[position]["unites"]:
            tuiles[position]["unites"][player] = {}

        if unit_type not in tuiles[position]["unites"][player]:
            tuiles[position]["unites"][player][unit_type] = {}

        existing_units = tuiles[position]["unites"][player][unit_type]
        new_unit_id = max(existing_units.keys(), default=-1) + 1

        tuiles[position]["unites"][player][unit_type][new_unit_id] = {"HP": units_dict[unit_type]['hp']}




    def add_unit_to_queue(self, unit_type, player, building_position):
        temps_creation = units_dict[unit_type]["temps_entrainement"]
        creation_time = temps_creation

        tile = tuiles.get(building_position, {})
        if "unit_creation_queue" not in tile:
            tile["unit_creation_queue"] = []

        tile["unit_creation_queue"].append({
            "type": unit_type,
            "player": player,
            "time_started": None,  # Enregistrez l'heure actuelle
            "creation_time": creation_time
        })



    def get_building_type_from_position(self, position):
        """Récupère le type de bâtiment et l'origine à partir d'une position donnée."""
        tile = tuiles.get(position, {})  # Récupérer la tuile à partir de la position

        # Vérifier si la tuile contient des bâtiments
        if "batiments" in tile:
            for player, buildings in tile["batiments"].items():
                for building_type, building_data in buildings.items():
                    # Vérifier que le bâtiment a une clé "parent" et récupérer l'origine
                    if "parent" in building_data:
                        origin = building_data["parent"]  # Récupérer la position du bâtiment principal
                        origin_tile = tuiles.get(origin, {})  # Récupérer la tuile de l'origine (bâtiment principal)

                        # Si l'origine est valide, on peut obtenir le type de bâtiment
                        if origin_tile and "batiments" in origin_tile:
                            for player_origin, buildings_origin in origin_tile["batiments"].items():
                                for origin_building_type, origin_building_data in buildings_origin.items():
                                    # Retourner le type de bâtiment trouvé à l'origine
                                    return origin_building_type, origin
                        else:
                            print(f"Aucune origine valide trouvée pour la tuile à {origin}.")
        return None, None

    def update_creation_times(self):
        current_time = time.time()  # Obtenez le temps actuel
        for position, tile in list(tuiles.items()):  # Utilisez list() pour éviter des erreurs lors de modifications
            if "unit_creation_queue" in tile:
                queue = tile["unit_creation_queue"]

                # Traiter uniquement la première unité dans la file d'attente
                if queue:
                    first_unit = queue[0]

                    # Démarrer la création si elle n'a pas encore commencé
                    if first_unit.get("time_started") is None:
                        first_unit["time_started"] = current_time
                        print(
                            f"Début de la création de l'unité {first_unit['type']} pour {first_unit['player']} à {position}.")

                    # Calculer le temps écoulé pour la première unité
                    elapsed_time = current_time - first_unit["time_started"]

                    # Si la première unité est terminée
                    if elapsed_time >= first_unit["creation_time"]:
                        # Obtenir le type de bâtiment et sa taille
                        building_type, origin = self.get_building_type_from_position(position)
                        if not building_type:
                            print(f"Aucun type de bâtiment trouvé à la position {position}.")
                            continue
                        building_size = builds_dict.get(building_type, {}).get('taille', 1)

                        # Calculer toutes les positions occupées par le bâtiment
                        building_positions = [
                            (origin[0] + dx, origin[1] + dy)
                            for dx in range(building_size)
                            for dy in range(building_size)
                        ]

                        # Liste des positions adjacentes par priorité
                        adjacent_positions = set()

                        # Ajouter toutes les cases adjacentes directement autour du bâtiment
                        for building_pos in building_positions:
                            x, y = building_pos
                            # Positions adjacentes immédiates
                            for adj_pos in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                                if adj_pos not in building_positions:  # Ignorer les cases du bâtiment
                                    adjacent_positions.add(adj_pos)

                        # Passer à un rayon croissant uniquement si nécessaire
                        radius = 1
                        while True:
                            # Ajouter des positions pour le rayon actuel
                            if radius > 1:
                                for building_pos in building_positions:
                                    for dx in range(-radius, radius + 1):
                                        for dy in range(-radius, radius + 1):
                                            adj_pos = (building_pos[0] + dx, building_pos[1] + dy)
                                            if adj_pos not in building_positions:
                                                adjacent_positions.add(adj_pos)

                            # Rechercher une position vide
                            for adj_pos in sorted(adjacent_positions):  # Tri optionnel pour un placement plus stable
                                if self.is_tile_empty(adj_pos):
                                    self.add_unit_to_tile(first_unit["type"], first_unit["player"], adj_pos)
                                    print(f"Unité {first_unit['type']} placée pour {first_unit['player']} à {adj_pos}.")
                                    queue.pop(0)  # Retirer l'unité de la file d'attente
                                    break
                            else:
                                # Si aucune tuile vide n'est trouvée dans ce rayon, augmenter le rayon
                                radius += 1
                                print(f"Aucune tuile vide trouvée à un rayon de {radius - 1}, augmentation à {radius}.")
                                continue

                            # Si une unité a été placée, arrêter la recherche
                            break

                        # Supprimer la clé "unit_creation_queue" si la liste est vide
                        if not queue:
                            del tile["unit_creation_queue"]
                            print(f"File d'attente vidée et supprimée pour {position}.")

    def show_remaining_time(self):
        current_time = time.time()
        for position, tile in tuiles.items():
            if "unit_creation_queue" in tile and tile["unit_creation_queue"]:
                first_unit = tile["unit_creation_queue"][0]
                if first_unit.get("time_started") is not None:
                    remaining_time = first_unit["creation_time"] - (current_time - first_unit["time_started"])
                    if remaining_time > 0:
                        print(
                            f"Unité {first_unit['type']} en cours pour {first_unit['player']} à {position}. Temps restant : {int(remaining_time)} sec")




