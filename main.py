from Game import Game
from constants import *


# Initialisation et lancement du jeu
if __name__ == "__main__":

    game = Game(screen_width, screen_height, map_size, minimap_size)
    game.run()
