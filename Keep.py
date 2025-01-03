class Keep(Buildings):
    def __init__(self, image, position, lettre='K', cout={'Wood': 35, 'Gold': 125}, hp=800, taille=1, build_time=80):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.attack = 5
        self.range = 8