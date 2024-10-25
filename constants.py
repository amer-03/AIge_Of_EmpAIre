import pygame

pygame.init()



info = pygame.display.Info()
screen_width = info.current_w  # Largeur de l'écran
screen_height = info.current_h  # Hauteur de l'écran

DISPLAYSURF = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
FPSCLOCK = pygame.time.Clock()

minimap_size = 50
map_size = 120

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)