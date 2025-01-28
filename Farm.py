from Buildings import Buildings

class Farm(Buildings):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def __init__(self, image, position, letter='F', cost={'Gold':0, 'Wood':60}, construction_time=10, hp=100, size=(2,2), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.contains_food=300
=======
    def __init__(self, image, position, lettre='F', cout={'Wood': 60}, hp=100, taille=2, build_time=10):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.food_remaining = 300
        self.walkable = True
>>>>>>> Stashed changes
=======
    def __init__(self, image, position, lettre='F', cout={'Wood': 60}, hp=100, taille=2, build_time=10):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.food_remaining = 300
        self.walkable = True
>>>>>>> Stashed changes
