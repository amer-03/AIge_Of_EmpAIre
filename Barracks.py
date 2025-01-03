from Buildings import Buildings

class Barracks(Buildings):
    def __init__(self, image, position, letter='B', cost={'Gold':0, 'Wood':175}, construction_time=50, hp=500, size=(3,3), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.spawn_swordsmen = True