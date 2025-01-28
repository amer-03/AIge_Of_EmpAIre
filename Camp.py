from Buildings import Buildings

class Camp(Buildings):
    def __init__(self, image, position, lettre='C', cout={'Wood': 100}, hp=200, taille=2, build_time=25):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.is_droppoint = True