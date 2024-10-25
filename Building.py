import time

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
        super().__init__(wood_cost=20, gold_cost=10, construction_time=180, hp=1000, size=(4, 4), population_cap_increase=20)
        self.villagers = []  # List to store created villagers
        self.villager_creation_time = 5  # Time to create each villager (in seconds)
    def create_villager(self, count):
        for i in range(count):
            print(f"Creating villager {i+1}/{count}...")
            time.sleep(self.villager_creation_time)  # Simulate time taken to create each villager
            self.villagers.append(1)
            print(f"Villager {i+1} created!")

class House(Building):
    def __init__(self):
        super().__init__(wood_cost=25, gold_cost=0, construction_time=25, hp=200, size=(2, 2), population_cap_increase=5)

    def __str__(self):
        """
        Returns a string representation of the House object.
        """
        return (f"House Details:\n"
                f"Cost: {self.wood_cost} wood\n"
                f"Build Time: {self.construction_time} seconds\n"
                f"HP: {self.hp}\n"
                f"Size: {self.size[0]}x{self.size[1]}\n"
                f"Functionality: Increases population cap by {self.population_cap_increase}\n")

class Camp(Building):
    def __init__(self):
        super().__init__(wood_cost=100, gold_cost=0, construction_time=25, hp=200, size=(2, 2), population_cap_increase=0)
        self.is_drop_point = True  # Indicates that this building serves as a drop point for resources

    def __str__(self):
        """
        Returns a string representation of the Camp object.
        """
        return (f"Camp Details:\n"
                f"Cost: {self.wood_cost} wood\n"
                f"Build Time: {self.construction_time} seconds\n"
                f"HP: {self.hp}\n"
                f"Size: {self.size[0]}x{self.size[1]}\n"
                f"Functionality: Drop point for resources\n"
                f"Population Cap Increase: {self.population_cap_increase}")

class Farm(Building):
    def __init__(self):
        super().__init__(wood_cost=60, gold_cost=0, construction_time=10, hp=100, size=(2, 2), population_cap_increase=0)
        self.food_capacity = 300  # Total food available in the farm

    def harvest_food(self, amount):
        """
        Harvest a specified amount of food from the farm.
        
        :param amount: The amount of food to harvest.
        :return: The actual amount of food harvested.
        """
        if amount <= self.food_capacity:
            self.food_capacity -= amount
            print(f"Harvested {amount} food. Remaining food: {self.food_capacity}.")
            return amount
        else:
            harvested = self.food_capacity
            self.food_capacity = 0
            print(f"Harvested {harvested} food. The farm is now empty.")
            return harvested

    def __str__(self):
        """
        Returns a string representation of the Farm object.
        """
        return (f"Farm Details:\n"
                f"Cost: {self.wood_cost} wood\n"
                f"Build Time: {self.construction_time} seconds\n"
                f"HP: {self.hp}\n"
                f"Size: {self.size[0]}x{self.size[1]}\n"
                f"Functionality: Contains {self.food_capacity} food\n"
                f"Population Cap Increase: {self.population_cap_increase}")

class Barracks(Building):
    def __init__(self):
        super().__init__(wood_cost=175, gold_cost=0, construction_time=50, hp=500, size=(3, 3), population_cap_increase=0)
        self.swordsmen = []  # List to keep track of swordsmen produced
        self.swordsman_creation_time = 10  # Time to create each swordsman (in seconds)

    def spawn_swordsman(self, count=1):
        """
        Spawns a specified number of swordsmen with a delay for each.
        
        :param count: Number of swordsmen to create.
        """
        for i in range(count):
            print(f"Spawning swordsman {i+1}/{count}...")
            time.sleep(self.swordsman_creation_time)  # Simulate time taken to spawn each swordsman
            self.swordsmen.append(1)
            print(f"Swordsman {i+1} spawned!")

    def list_swordsmen(self):
        """
        Lists all swordsmen created by the Barracks.
        """
        if self.swordsmen:
            print("List of swordsmen and their tasks:")
            for swordsman in self.swordsmen:
                print(f"- {swordsman}")
        else:
            print("No swordsmen have been spawned yet.")

    def __str__(self):
        """
        Returns a string representation of the Barracks object.
        """
        return (f"Barracks Details:\n"
                f"Cost: {self.wood_cost} wood\n"
                f"Build Time: {self.construction_time} seconds\n"
                f"HP: {self.hp}\n"
                f"Size: {self.size[0]}x{self.size[1]}\n"
                f"Functionality: Spawns Swordsmen\n"
                f"Population Cap Increase: {self.population_cap_increase}")



#farm = Farm()
#print(farm)
#farm.harvest_food(100)
#print(farm)
#town_center = TownCentre () 
#town_center.create_villager(3)
#barrack = Barracks()
#barrack.spawn_swordsman(3)
