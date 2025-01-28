from Buildings import Buildings

class House(Buildings):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def __init__(self, image, position, letter='H', cost={'Gold':0, 'Wood':25}, construction_time=25, hp=200, size=(2,2), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.population_cap_increase=5
=======
    def __init__(self, image, position, lettre='H', cout={'Wood': 25}, hp=200, taille=2, build_time=25, population=5):
        super().__init__(image, position, lettre, cout, hp, taille, build_time, population)
>>>>>>> Stashed changes
=======
    def __init__(self, image, position, lettre='H', cout={'Wood': 25}, hp=200, taille=2, build_time=25, population=5):
        super().__init__(image, position, lettre, cout, hp, taille, build_time, population)
>>>>>>> Stashed changes
