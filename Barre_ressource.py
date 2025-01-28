import pygame
from constants import *

class Barre_ressources:
    def __init__(self, image_path, text, font_size):
        self.image = pygame.image.load(image_path)  # Charger l'image
        self.image = pygame.transform.scale(self.image, (screen_height//21.6, screen_height//21.6))  # Redimensionner l'image

        self.text = text
        self.font = pygame.font.Font(None, font_size)  # Police avec la taille donnée

        self.barre_width = screen_width//3  # Largeur de la barre
        self.color = BLACK
        self.color_barre_units = GRAY
        self.image_barre_units = pygame.transform.scale(self.image, (screen_height//27, screen_height//27))  # Redimensionner l'image

        self.color_barre_builds = LIGHT_GRAY
        self.image_barre_builds = pygame.transform.scale(self.image, (screen_height//27, screen_height//27))  # Redimensionner l'image

    def draw_title(self, surface, text, x, y, color):
        # Rendre le texte
        title = self.font.render(text, True, color)

        # Calculer les coordonnées pour centrer le texte
        title_x = x + (self.barre_width - title.get_width()) // 2
        title_y = y - title.get_height() - 5  # Légèrement au-dessus de la barre

        # Dessiner le texte sur la surface
        surface.blit(title, (title_x, title_y))

    def barre(self, surface, x, y):
        # Dessine un rectangle noir à la position (x, y)
        pygame.draw.rect(surface, self.color, (x, y, barre_width, barre_height))

    def draw(self, surface, x_barre, y_barre, compteur, index, total_images):
        # Calculer l'espacement pour répartir les images
        espace = barre_width // total_images  # Espacement égal entre chaque image

        # Calculer la position x de chaque image en fonction de son index
        x_image = x_barre + (espace * index) + (espace - self.image.get_width()) // 2
        y_image = y_barre

        # Afficher l'image
        surface.blit(self.image, (x_image, y_image))

        # Générer le texte avec le compteur
        texte = self.font.render(f" {compteur}", True, (255, 255, 255))  # Texte en blanc

        # Centrer le texte sous l'image
        text_x = x_image + (self.image.get_width() - texte.get_width()) // 2
        text_y = y_image + self.image.get_height() + 5  # Placer juste en dessous de l'image

        # Afficher le texte
        surface.blit(texte, (text_x, text_y))

    def barre_units(self, surface, x, y):
        pygame.draw.rect(surface, self.color_barre_units, (x, y, barre_units_width, barre_units_height))

    def draw_barre_units(self, surface, x_barre, y_barre, compteur, index, total_images):
        espace = barre_width // total_images  # Espacement égal entre chaque image

        # Calculer la position x de chaque image en fonction de son index
        x_image = x_barre + (espace * index) + (espace - self.image_barre_units.get_width() ) // 2
        y_image = y_barre

        # Afficher l'image
        surface.blit(self.image_barre_units, (x_image, y_image))

        # Générer le texte avec le compteur
        texte = self.font.render(f" {compteur}", True, (255, 255, 255))  # Texte en blanc

        # Centrer le texte sous l'image
        text_x = x_image + self.image_barre_units.get_width()
        text_y = y_image + self.image_barre_units.get_height() // 2   # Placer juste en dessous de l'image

        # Afficher le texte
        surface.blit(texte, (text_x, text_y))

    def barre_builds(self, surface, x, y):
        pygame.draw.rect(surface, self.color_barre_builds, (x, y, barre_units_width, barre_units_height))

