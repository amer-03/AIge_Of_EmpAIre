from Buildings import Buildings

class House(Buildings):
    def __init__(self, image, position, lettre='H', cout={'Wood': 25}, hp=200, taille=2, build_time=25, population=5):
        super().__init__(image, position, lettre, cout, hp, taille, build_time, population)