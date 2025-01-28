from Buildings import Buildings

class TownCenter(Buildings):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def __init__(self, image, position, letter='T', cost={'Gold':0, 'Wood':350}, construction_time=150, hp=1000, size=(4,4), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.population_cap_increase=5
        self.drop_point_ressources=True
=======
    def __init__(self, image, position, lettre='T', cout={'Wood': 350}, hp=1000, taille=4, build_time=150, population=5):
        super().__init__(image, position, lettre, cout, hp, taille, build_time, population)
        self.can_spawn_villagers = True
        self.is_droppoint = True
>>>>>>> Stashed changes
=======
    def __init__(self, image, position, lettre='T', cout={'Wood': 350}, hp=1000, taille=4, build_time=150, population=5):
        super().__init__(image, position, lettre, cout, hp, taille, build_time, population)
        self.can_spawn_villagers = True
        self.is_droppoint = True
>>>>>>> Stashed changes
