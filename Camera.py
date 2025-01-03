from constants import *
from pygame.locals import *

class Camera:
    def __init__(self):
            self.cam_x=0
            self.cam_y=0
            self.scroll_speed = 30

    def center_camera_on_tile(self):
        center_x = size // 2
        center_y = size // 2
        cart_x = center_x * tile_grass.width_half
        cart_y = center_y * tile_grass.height_half
        iso_x = (cart_x - cart_y)
        iso_y = (cart_x - cart_y) // 2
        self.cam_x = (iso_x - screen_width // 2) + tile_grass.width_half
        self.cam_y = -(iso_y + screen_height // 2)
           
    def calculate_camera_limits(self):
        """Calcule les limites de la caméra pour empêcher le défilement hors de la carte."""
        # Taille de la moitié de la carte

        # Calcul des coins en coordonnées cartésiennes
        min_cart_x = -half_size * tile_grass.width_half
        max_cart_x = half_size * tile_grass.width_half
        min_cart_y = -half_size * tile_grass.height_half
        max_cart_y = half_size * tile_grass.height_half

        # Conversion des coins en isométriques
        min_iso_x = min_cart_x - max_cart_y
        max_iso_x = max_cart_x - min_cart_y
        min_iso_y = (min_cart_x + min_cart_y) // 2
        max_iso_y = (max_cart_x + max_cart_y) // 2

        # Ajustement pour la taille de l'écran
        min_cam_x = min_iso_x - (screen_width // 2) + screen_width // 2 + (-5 * tile_grass.width_half)
        max_cam_x = max_iso_x - (screen_width // 2) - screen_width // 2 + 5 * tile_grass.width_half
        min_cam_y = min_iso_y - (screen_height // 2) + screen_height // 2 + (-5 * tile_grass.width_half)
        max_cam_y = max_iso_y - (screen_height // 2) - screen_height // 2 + 5 * tile_grass.width_half

        return min_cam_x, min_cam_y, max_cam_x, max_cam_y
    
    def handle_camera_movement(self, keys):
        min_cam_x, min_cam_y, max_cam_x, max_cam_y = self.calculate_camera_limits()
        speed = self.scroll_speed * 2 if keys[K_LSHIFT] or keys[K_RSHIFT] else self.scroll_speed
        if keys[K_q]:
            self.cam_x = max(self.cam_x - speed, min_cam_x)  # Déplace à gauche
        if keys[K_d]:
            self.cam_x = min(self.cam_x + speed, max_cam_x)  # Déplace à droite
        if keys[K_z]:
            self.cam_y = max(self.cam_y - speed, min_cam_y)  # Déplace vers le haut
        if keys[K_s]:
            self.cam_y = min(self.cam_y + speed, max_cam_y)  # Déplace vers le bas