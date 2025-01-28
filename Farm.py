from Buildings import Buildings

class Farm(Buildings):
    def __init__(self, image, position, lettre='F', cout={'Wood': 60}, hp=100, taille=2, build_time=10):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.food_remaining = 300
        self.walkable = True