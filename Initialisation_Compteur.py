from constants import *
from TileMap import TileMap
from Barre_ressource import Barre_ressources
from Units import Units
from Buildings import Buildings
import threading
import time
import keyboard
import curses

class Initialisation_Compteur:

    def __init__(self):
        self.barre_ressources = Barre_ressources
        self.compteur = compteurs_joueurs
        self.barres = [
            Barre_ressources("images/bois_barre.png", "w", screen_height // 45),
            Barre_ressources("images/or_barre.png", "g", screen_height // 45),
            Barre_ressources("images/food_barre.png", "f", screen_height // 45),
            Barre_ressources("images/entite.png", "U", screen_height // 45)
        ]

        self.barre_units = [
            Barre_ressources("images/villageois.webp", "v", screen_height // 45),
            Barre_ressources("images/epeiste.png", "s", screen_height // 45),
            Barre_ressources("images/cavalier.png", "h", screen_height // 45),
            Barre_ressources("images/archer.png", "a", screen_height // 45)
        ]

        self.barre_builds = [
            Barre_ressources("images/Town_Center.webp", "T", screen_height // 45),
            Barre_ressources("images/House.webp", "H", screen_height // 45),
            Barre_ressources("images/Camp.png", "C", screen_height // 45),
            Barre_ressources("images/Farm - Copie.png", "f", screen_height // 45),
            Barre_ressources("images/Barracks.png", "B", screen_height // 45),
            Barre_ressources("images/Stable.png", "S", screen_height // 45),
            Barre_ressources("images/Archery Range.png", "A", screen_height // 45),
            Barre_ressources("images/Keep.png", "K", screen_height // 45)
        ]

        self.f1_active = False
        self.f2_active = False
        self.f3_active = False

    def create_count(self,n):
        for i in range(1, n + 1):
            # Crée un dictionnaire de compteurs pour chaque joueur
            compteurs_joueurs[f'joueur_{i}'] = {
                # Ressources
                'ressources': {
                    'W': 0,  # Bois
                    'f': 0,  # Nourriture
                    'G': 0,  # Or
                    'U': 0,  # Unités générales (ou autre ressource spéciale)
                    'max_pop': 195
                },
                # Unités
                'unites': {
                    'v': 0,  # Villageois
                    's': 0,  # Swordsman (épéiste)
                    'h': 0,  # Horseman (cavalier)
                    'a': 0  # Archer
                },
                # Bâtiments
                'batiments': {
                    'T': 0,  # Tour de guet
                    'H': 0,  # Maison
                    'C': 0,  # Centre-ville
                    'F': 0,  # Ferme
                    'B': 0,  # Caserne
                    'S': 0,  # Forge
                    'A': 0,  # Académie
                    'K': 0  # Château
                }
            }
    def update_compteur(self):
        for joueur, compteurs in compteurs_joueurs.items():
            if isinstance(compteurs['unites'], dict):
                compteurs['ressources']['U'] = sum(compteurs['unites'].values())

    def initialize_resources(self, unit,n):
        self.create_count(n)
        # Parcourt chaque joueur dans le dictionnaire pour initialiser les ressources
        for joueur, compteurs in compteurs_joueurs.items():
            if unit == "Lean":
                compteurs['ressources']['W'] = 6000
                compteurs['ressources']['f'] = 1150
                compteurs['ressources']['G'] = 1150
                compteurs['unites']['v'] = 2
                compteurs['unites']['a'] = 0
                if isinstance(compteurs['unites'], dict):
                    compteurs['ressources']['U'] = sum(compteurs['unites'].values())
                compteurs['batiments']['T'] = 1
                compteurs['batiments']['B'] = 0
                compteurs['batiments']['S'] = 0
                compteurs['batiments']['K'] = 0
                compteurs['batiments']['H'] = 0
                compteurs['batiments']['A'] = 0
                compteurs['batiments']['F'] = 1

            elif unit == "Mean":
                compteurs['ressources']['W'] = 2000
                compteurs['ressources']['f'] = 2000
                compteurs['ressources']['G'] = 2000
                compteurs['unites']['v'] = 3
                compteurs['unites']['a'] = 3
                if isinstance(compteurs['unites'], dict):
                    compteurs['ressources']['U'] = sum(compteurs['unites'].values())
                compteurs['batiments']['T'] = 1
            elif unit == "Marines":
                compteurs['ressources']['W'] = 20000
                compteurs['ressources']['f'] = 20000
                compteurs['ressources']['G'] = 20000
                compteurs['unites']['v'] = 15
                if isinstance(compteurs['unites'], dict):
                    compteurs['ressources']['U'] = sum(compteurs['unites'].values())
                compteurs['batiments']['T'] = 3
                compteurs['batiments']['B'] = 2
                compteurs['batiments']['S'] = 2
                compteurs['batiments']['A'] = 2

    def draw_ressources(self):
        x_barre_base = 100  # Position de départ en X pour la première colonne
        y_barre_base = 40  # Position de départ en Y pour la première ligne

        espacement_horizontal = barre_width + screen_width//9.6  # Espacement entre les colonnes
        espacement_vertical = barre_height + screen_height // 9.6  # Espacement entre les lignes

        total_images = len(self.barres)
        total_images_barre_builds = len(self.barre_builds)

        for index, (joueur, compteurs) in enumerate(compteurs_joueurs.items()):
            # Calcul de la position en X et Y pour chaque joueur
            colonne = index % 2  # 0 pour la première colonne, 1 pour la seconde
            ligne = index // 2  # Numéro de la ligne

            x_barre = x_barre_base + colonne * espacement_horizontal
            y_barre = y_barre_base + ligne * espacement_vertical

            # Affiche les ressources (f1_active)
            if self.f1_active:
                self.barres[0].barre(DISPLAYSURF, x_barre, y_barre)
                for i, barre in enumerate(self.barres):
                    type = ["W", "G", "f", "U"][i]
                    if type == "U":
                        max_value=self.compteur[joueur]['ressources']['max_pop']
                        barre.draw(DISPLAYSURF, x_barre, y_barre, self.compteur[joueur]['ressources'][type], i,
                               total_images,max_value)
                        color = PLAYER_COLORS.get(joueur, (255, 255, 255))
                        barre.draw_title(DISPLAYSURF, joueur, x_barre, y_barre,color)
                    else :
                        barre.draw(DISPLAYSURF, x_barre, y_barre, self.compteur[joueur]['ressources'][type], i,
                                   total_images, None)
                        color = PLAYER_COLORS.get(joueur, (255, 255, 255))
                        barre.draw_title(DISPLAYSURF, joueur, x_barre, y_barre, color)

            # Affiche les unités (f2_active)
            if self.f2_active:
                for barre_unit in self.barres:
                    barre_unit.barre_units(DISPLAYSURF, x_barre, y_barre + barre_height)
                for i, barre in enumerate(self.barre_units):
                    type = ["v", "s", "h", "a"][i]
                    barre.draw_barre_units(DISPLAYSURF, x_barre, y_barre + barre_height,
                                       self.compteur[joueur]['unites'][type], i, total_images)


            # Affiche les constructions (f3_active)
            if self.f3_active:
                for barre_builds in self.barres:
                    barre_builds.barre_builds(DISPLAYSURF, x_barre, y_barre + barre_height + barre_units_height)
                for i, barre in enumerate(self.barre_builds):
                    type = ["T", "H", "C", "F", "B", "S", "A", "K"][i]
                    barre.draw_barre_units(DISPLAYSURF, x_barre, y_barre + barre_height + barre_units_height,
                                           self.compteur[joueur]['batiments'][type], i, total_images_barre_builds)
