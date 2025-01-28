<<<<<<< Updated upstream
<<<<<<< Updated upstream
from Buildings import Buildings

class Keep(Buildings):
    def __init__(self, image, position, letter='K', cost={'Gold':125, 'Wood':35}, construction_time=80, hp=800, size=(1,1), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.fire_arrows = {'attack':5 , 'range':8}
=======
=======
>>>>>>> Stashed changes
class Keep(Buildings):
    def __init__(self, image, position, lettre='K', cout={'Wood': 35, 'Gold': 125}, hp=800, taille=1, build_time=80):
        super().__init__(image, position, lettre, cout, hp, taille, build_time)
        self.attack = 5
<<<<<<< Updated upstream
        self.range = 8
>>>>>>> Stashed changes
=======
        self.range = 8
>>>>>>> Stashed changes
