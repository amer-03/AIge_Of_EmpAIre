from Buildings import Buildings

class Keep(Buildings):
    def __init__(self, image, position, letter='K', cost={'Gold':125, 'Wood':35}, construction_time=80, hp=800, size=(1,1), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.fire_arrows = {'attack':5 , 'range':8}