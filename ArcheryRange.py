from Buildings import Buildings

class ArcheryRange(Buildings):
    def __init__(self, image, position, letter='A', cost={'Gold':0, 'Wood':175}, construction_time=50, hp=500, size=(3,3), population_cap_increase=0, drop_point_ressources=False, walkable=False):
        super().__init__(image, position, letter, cost, construction_time, hp, size, population_cap_increase, drop_point_ressources, walkable)
        self.spawn_archer = True