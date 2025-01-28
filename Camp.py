from Buildings import Buildings

class Camp(Buildings):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def __init__(self, image, position, letter='C', cost={'Gold':0, 'Wood':100}, construction_time=25, hp=200, size=(2,2), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.drop_point_ressources=True
=======
    def __init__(self, image, position, lettre='C', cout={'Wood': 100}, hp=200, taille=2, build_time=25):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.is_droppoint = True
>>>>>>> Stashed changes
=======
    def __init__(self, image, position, lettre='C', cout={'Wood': 100}, hp=200, taille=2, build_time=25):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.is_droppoint = True
>>>>>>> Stashed changes
