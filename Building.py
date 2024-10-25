class Building:
    def __init__(self, wood_cost, gold_cost, construction_time, hp, size, population_cap_increase):
        """
        Initializes a Building object with specified attributes.
        
        :param wood_cost: The amount of wood required for construction.
        :param gold_cost: The amount of gold required for construction.
        :param construction_time: Time required to construct the building.
        :param hp: Hit points (health) of the building.
        :param size: Tuple representing the size of the building (width, height).
        :param population_cap_increase: The amount of population cap this building adds.
        """
        self.wood_cost = wood_cost
        self.gold_cost = gold_cost
        self.construction_time = construction_time
        self.hp = hp
        self.size = size  # tuple (width, height)
        self.population_cap_increase = population_cap_increase
    
    def __str__(self):
        """
        Returns a string representation of the Building object.
        """
        return (f"Building Details:\n"
                f"Cost: {self.wood_cost} wood, {self.gold_cost} gold\n"
                f"Construction Time: {self.construction_time} seconds\n"
                f"HP: {self.hp}\n"
                f"Size: {self.size[0]}x{self.size[1]}\n"
                f"Population Cap Increase: {self.population_cap_increase}")
    
    def total_cost(self):
        """
        Returns the total cost of the building (wood + gold).
        """
        return self.wood_cost + self.gold_cost

class TownCentre(Building):
    def __init__(self):
        super().__init__(350,0,150,1000,(4,4),5)
    def create_villager(self, count):
        for _ in range(count):