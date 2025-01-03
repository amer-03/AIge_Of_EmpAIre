from math import sqrt
import math
import pygame
from TileMap import *
from constants import *
from Coordinates import *
from Units import *
import random
import time

class Recolte_ressources:
    def __init__(self):
        self.tile_grass = tile_grass
        self.unit=Unit()

    def trouver_plus_proche_ressource(self, joueur, type_unite, id_unite, ressource):
        position_unite = None
        for position, data in tuiles.items():
            if 'unites' in data and joueur in data['unites']:
                unites_joueur = data['unites'][joueur]
                if type_unite in unites_joueur and id_unite in unites_joueur[type_unite]:
                    position_unite = position
                    break

        if position_unite is None:
            return None  # Unité non trouvée

        # Collecter toutes les positions des ressources 'G' qui sont disponibles (quantité > 0)
        positions_ressources = []
        for position, data in tuiles.items():
            if 'ressources' in data and data['ressources'] == ressource and data.get('quantite', 0) > 0:
                positions_ressources.append(position)
        def distance(pos1, pos2):
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])  # Distance de Manhattan

        plus_proche = None
        distance_minimale = float('inf')
        for pos in positions_ressources:
            dist = distance(position_unite, pos)
            if dist < distance_minimale:
                distance_minimale = dist
                plus_proche = pos

        return plus_proche

    def trouver_plus_proche_batiment(self, joueur, type_unite, id_unite):
        # Trouver la position de l'unité
        position_unite = None
        for position, data in tuiles.items():
            if 'unites' in data and joueur in data['unites']:
                unites_joueur = data['unites'][joueur]
                if type_unite in unites_joueur and id_unite in unites_joueur[type_unite]:
                    position_unite = position
                    break

        if position_unite is None:
            return None  # Unité non trouvée

        # Rechercher les positions des bâtiments appartenant au joueur
        positions_batiments = []
        for position, data in tuiles.items():
            if 'batiments' in data and joueur in data['batiments']:
                for type_b, infos in data['batiments'][joueur].items():
                    if type_b in ['T', 'C']:  # Rechercher uniquement les types 'T' et 'C'
                        positions_batiments.append(position)

        if not positions_batiments:
            return None  # Aucun bâtiment appartenant au joueur trouvé

        # Trouver le bâtiment le plus proche
        def distance(pos1, pos2):
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])  # Distance de Manhattan

        plus_proche = None
        distance_minimale = float('inf')
        for pos in positions_batiments:
            dist = distance(position_unite, pos)
            if dist < distance_minimale:
                distance_minimale = dist
                plus_proche = pos

        return plus_proche

    def recolter_ressource_plus_proche_via_trouver(self, joueur, type_unite, id_unite, posress,
                                                   recolte_max=20):
        if posress is None:
            return "Aucune ressource disponible à proximité."
        position_unite = None
        for position, data in tuiles.items():
            if 'unites' in data and joueur in data['unites']:
                unites_joueur = data['unites'][joueur]
                if type_unite in unites_joueur and id_unite in unites_joueur[type_unite]:
                    position_unite = position
                    break

        if position_unite is None:
            return "Unité introuvable."

        details_ressource = tuiles[posress]
        quantite_a_recolter = min(recolte_max, details_ressource['quantite'])
        details_ressource['quantite'] -= quantite_a_recolter
        if details_ressource is None or 'quantite' not in details_ressource or details_ressource['quantite'] <= 0:
            del tuiles[posress]['ressources']
            del tuiles[posress]['quantite']# Supprimer la tuile si la quantité est 0

        unite = tuiles[position_unite]['unites'][joueur][type_unite][id_unite]

        unite['capacite'] = str(int(unite['capacite']) + quantite_a_recolter)

        if action_a_executer:
            action = action_a_executer.pop(0)
            action()


    def deposer_ressources(self, quantite, joueur, type_unite, id_unite, ressource):
        position_unite = None
        for position, data in tuiles.items():
            if 'unites' in data and joueur in data['unites']:
                unites_joueur = data['unites'][joueur]
                if type_unite in unites_joueur and id_unite in unites_joueur[type_unite]:
                    position_unite = position
                    break
        compteurs_joueurs[joueur]['ressources'][ressource] += quantite
        unite = tuiles[position_unite]['unites'][joueur][type_unite][id_unite]
        unite['capacite'] = 0