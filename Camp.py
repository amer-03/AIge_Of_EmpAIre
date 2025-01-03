from Buildings import Buildings

class Camp(Buildings):
    def __init__(self, image, position, letter='C', cost={'Gold':0, 'Wood':100}, construction_time=25, hp=200, size=(2,2), walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, walkable)
        self.drop_point_ressources=True