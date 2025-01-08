from constants import *

class Coordinates:
    """Classe gérant les coordonnées."""

    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def to_tuple(self):
        t=(self.x,self.y)
        return t
    
    def to_iso(self,cam_x,cam_y):
        half_size = size // 2  # Assurez-vous que la taille de la carte est correctement définie

        # Décalage centré pour le joueur
        centered_col = self.y - half_size
        centered_row = self.x - half_size

        # Conversion en coordonnées isométriques
        cart_x = centered_row * tile_grass.width_half
        cart_y = centered_col * tile_grass.height_half

        iso_x = cart_x - cart_y-cam_x # Ne pas soustraire cam_x ici
        iso_y = (cart_x + cart_y) / 2  -cam_y
        return iso_x,iso_y
    
    def __str__(self):
        return f"Position: {self.x},{self.y}"
    