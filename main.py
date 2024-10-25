
import pygame

from Game import Game
from constants import screen_width, screen_height


pygame.init()

# Configuration de l'écran et des FPS
info = pygame.display.Info()
screen_width = info.current_w  # Largeur de l'écran
screen_height = info.current_h  # Hauteur de l'écran

# Initialisation et lancement du jeu
if __name__ == "__main__":
    # Définition des dimensions de la carte et de la mini-carte
    map_size = 120
    minimap_size = 50

    # Création de l'instance de jeu et exécution
    game = Game(screen_width, screen_height, map_size, minimap_size)
