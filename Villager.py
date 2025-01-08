from Units import Units

class Villager(Units):
    def __init__(self, image,position, lettre="v", cout={'Gold': 0, 'Food': 50, 'Wood': 0}, hp=25, temps_entrainement= 25,attaque=2, range=1, vitesse=0.8):
        super().__init__(image, position, lettre, cout, hp, temps_entrainement, attaque, range, vitesse)
        
