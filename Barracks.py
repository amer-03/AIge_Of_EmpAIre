from Buildings import Buildings

class Barracks(Buildings):
    def __init__(self, image, position, lettre='B', cout={'Wood': 175}, hp=500, taille=3, build_time=50):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.can_spawn_swordsmen = True