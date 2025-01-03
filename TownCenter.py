from Buildings import Buildings

class TownCenter(Buildings):
    def __init__(self, image, position, letter='T', cost={'Gold':0, 'Wood':350}, construction_time=150, hp=1000, size=(4,4), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.population_cap_increase=5
        self.drop_point_ressources=True