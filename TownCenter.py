from Buildings import Buildings

class TownCenter(Buildings):
    def __init__(self, image, position, lettre='T', cout={'Wood': 350}, hp=1000, taille=4, build_time=150, population=5):
        super().__init__(image, position, lettre, cout, hp, taille, build_time, population)
        self.can_spawn_villagers = True
        self.is_droppoint = True