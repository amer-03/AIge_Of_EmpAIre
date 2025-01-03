from Buildings import Buildings

class Farm(Buildings):
    def __init__(self, image, position, letter='F', cost={'Gold':0, 'Wood':60}, construction_time=10, hp=100, size=(2,2), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.contains_food=300