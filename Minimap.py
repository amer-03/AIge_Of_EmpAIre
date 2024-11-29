import pygame

class Minimap:
    def __init__(self, scale_factor=0.2):
        self.scale_factor = scale_factor
        self.minimap_surface = pygame.Surface((490, 270))  # Match Game class sizes
        self.viewport_color = (255, 255, 255)
        self.main_map_size = None
        self.colors = {
            'H': (139, 69, 19),    
            'C': (128, 128, 128),
            'F': (34, 139, 34),
            'B': (165, 42, 42),
            'S': (210, 180, 140),
            'A': (0, 100, 0),
            'K': (47, 79, 79),
            'G': (255, 215, 0),
            'W': (139, 115, 85),
            ' ': (0, 0, 0)
        }
        
    def init_surface(self):
        self.minimap_surface = pygame.Surface(self.size)
        self.minimap_surface.fill((0, 0, 0))
        
    def update(self, map_data, camera_pos, viewport_size):
        self.minimap_surface.fill((0, 0, 0))
        
        # Draw map elements
        for y in range(len(map_data)):
            for x in range(len(map_data[y])):
                color = self.colors.get(map_data[y][x], (0, 0, 0))
                mini_x = int(x * self.scale_factor)
                mini_y = int(y * self.scale_factor)
                pygame.draw.rect(
                    self.minimap_surface,
                    color,
                    (mini_x, mini_y, max(1, int(self.scale_factor)), max(1, int(self.scale_factor)))
                )

        # Draw viewport rectangle
        viewport_x = int(camera_pos[0] * self.scale_factor)
        viewport_y = int(camera_pos[1] * self.scale_factor)
        viewport_w = int(viewport_size[0] * self.scale_factor)
        viewport_h = int(viewport_size[1] * self.scale_factor)
        
        pygame.draw.rect(
            self.minimap_surface,
            self.viewport_color,
            (viewport_x, viewport_y, viewport_w, viewport_h),
            1
        )

    def handle_click(self, click_pos):
        map_x = int(click_pos[0] / self.scale_factor)
        map_y = int(click_pos[1] / self.scale_factor)
        return (map_x, map_y)