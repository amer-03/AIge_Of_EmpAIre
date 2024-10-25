import pygame


class Tile:
    def __init__(self, image_path, width, height):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.width = width
        self.height = height
        self.width_half = width // 2
        self.height_half = height // 2
