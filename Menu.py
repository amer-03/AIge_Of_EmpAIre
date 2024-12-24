from constants import *

class menu():
    def __init__(self):
        self.selected_option = None
        self.menu_active = True
        self.selected_unit = None
        self.selected_map = None
        self.joueur = 0
        self.compteur = compteurs_joueurs
        self.n = 2  # Définition du nombre de joueurs
        self.dropdown_open = False  # Indicateur pour savoir si la liste déroulante est ouverte
        self.options_rects = []