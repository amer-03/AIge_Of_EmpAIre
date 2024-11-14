import math

class Unit :
    def __init__(self, cost, hp, attack, speed, training_time, position=(0, 0)):
        self.cost = cost                  # coût de l'unité en ressources
        self.hp = hp                      # points de vie (HP)
        self.attack = attack              # points d'attaque par seconde
        self.speed = speed                # vitesse en tiles par seconde
        self.training_time = training_time  # temps d'entrainement en secondes
        self.position = position    #position de l'unité sur la map
    
    def take_damage(self, damage):
        """Réduit les HP de l'unité en fonction des dégâts reçus."""
        self.hp = max(0, self.hp - damage)
        return self.hp == 0  # Retourne vrai si l'unité est détruite
    
    def move_to(self, new_position):
        """Déplace l'unité vers une nouvelle position"""
        self.position = new_position

class Villager(Unit):
    def __init__(self):
        super().__init__(cost={"F": 50}, hp=25, attack=2, speed=0.8, training_time=25)
        self.resource_rate = 25 / 60  # Collecte 25 unités/minute 
        self.carry_capacity = 20

    def build_time(self, t, n):
        """Calcule le temps de construction en fonction du nombre de villagers."""
        return (3 * t) / (n + 2)
    
    def collect_resources(self, resource, time_in_seconds):
        """Recolte des ressources en fonction du temp donné."""
        collected = min(time_in_seconds * self.resource_rate, self.carry_capacity)
        return {resource: collected}

class Swordsman(Unit):
    def __init__(self):
        super().__init__(cost={"F": 50, "G": 20}, hp=40, attack=4, speed=0.9, training_time=20)

class Horseman(Unit):
    def __init__(self):
        super().__init__(cost={"F": 80, "G": 20}, hp=45, attack=4, speed=1.2, training_time=30)

class Archer(Unit):
    def __init__(self):
        super().__init__(cost={"W": 25, "G": 45}, hp=30, attack=4, speed=1, training_time=35)
        self.range = 4 #Portée de l'attaque en distance euclidienne

    def is_in_range(self, target_position, archer_position):
        distance = math.sqrt((target_position[0] - archer_position[0]) ** 2 + (target_position[1] - archer_position[1]) ** 2)
        return distance <= self.range