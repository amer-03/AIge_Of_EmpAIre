from TileMap import *
from constants import *

class Coordinates:
    def __init__(self):
        self.x=0
        self.y=0

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def to_iso(self,x, y, cam_x, cam_y):
        half_size = size // 2  # Assurez-vous que la taille de la carte est correctement définie

        # Décalage centré pour le joueur
        centered_col = y - half_size
        centered_row = x - half_size

        # Conversion en coordonnées isométriques
        cart_x = centered_row * tile_grass.width_half
        cart_y = centered_col * tile_grass.height_half

        iso_x = cart_x - cart_y - cam_x  # Ne pas soustraire cam_x ici
        iso_y = (cart_x + cart_y) / 2 - cam_y # Ne pas soustraire cam_y ici

        #iso_x = (int(current_y - current_x)) * tile_grass.width - cam_x
        #iso_y = (int(current_x + current_y)//2) * tile_grass.height - cam_y
        return iso_x,iso_y