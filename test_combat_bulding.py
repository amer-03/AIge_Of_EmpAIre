from TownCenter import TownCenter 
from Units import Units
from Coordinates import Coordinates

# Créer un bâtiment (exemple : TownCenter)
building = TownCenter(
    image=None,  # Image fictive ou None
    position=Coordinates(10, 10)
)

# Créer une unité (exemple : un soldat)
unit = Units(
    image=None,  # Image fictive ou None
    position=Coordinates(12, 12),
    lettre="U",
    cout={"Gold": 50, "Wood": 20},
    hp=100,
    temps_entrainement=10,
    attaque=20,
    range=5,
    vitesse=1
)

# Afficher les informations initiales
print("=== ÉTAT INITIAL ===")
print(f"Building HP: {building.hp}")
print(f"Unit HP: {unit.hp}")

# Lancer l'attaque
unit.attack_building(building)

# Afficher les informations après l'attaque
print("\n=== ÉTAT APRÈS L'ATTAQUE ===")
print(f"Building HP: {building.hp}")
if building.image is None:
    print("Le bâtiment a été détruit !")

# Vérifier l'état de l'unité
print(f"Unit HP: {unit.hp}")
