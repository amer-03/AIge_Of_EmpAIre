from Buildings import Buildings

class ArcheryRange(Buildings):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def __init__(self, image, position, letter='A', cost={'Gold':0, 'Wood':175}, construction_time=50, hp=500, size=(3,3), population_cap_increase=0, drop_point_ressources=False, walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, population_cap_increase, drop_point_ressources, walkable)
        self.spawn_archer = True
=======
    def __init__(self, image, position, lettre='A', cout={'Wood': 175}, hp=500, taille=3, build_time=50):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.can_spawn_archers = True
>>>>>>> Stashed changes
=======
    def __init__(self, image, position, lettre='A', cout={'Wood': 175}, hp=500, taille=3, build_time=50):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.can_spawn_archers = True
>>>>>>> Stashed changes
