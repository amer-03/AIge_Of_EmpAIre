from Buildings import Buildings

class Barracks(Buildings):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def __init__(self, image, position, letter='B', cost={'Gold':0, 'Wood':175}, construction_time=50, hp=500, size=(3,3), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.spawn_swordsmen = True
=======
    def __init__(self, image, position, lettre='B', cout={'Wood': 175}, hp=500, taille=3, build_time=50):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.can_spawn_swordsmen = True
>>>>>>> Stashed changes
=======
    def __init__(self, image, position, lettre='B', cout={'Wood': 175}, hp=500, taille=3, build_time=50):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.can_spawn_swordsmen = True
>>>>>>> Stashed changes
