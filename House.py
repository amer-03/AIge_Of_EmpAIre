from Buildings import Buildings

class House(Buildings):
    def __init__(self, image, position, letter='H', cost={'Gold':0, 'Wood':25}, construction_time=25, hp=200, size=(2,2), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.population_cap_increase=5