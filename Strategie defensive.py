from Units import *
from Buildings import Buildings
from Recolte_ressources import *


class Strat_defensive:
    def __init__(self, player_id, game):
        self.player_id = f"joueur_{player_id}"
        self.game = game
        self.phase = 1

    def execute_defensive_strategy(self):
        if self.phase == 1:
            self.phase_1()
        elif self.phase == 2:
            self.phase_2()
        elif self.phase == 3:
            self.phase_3()
        elif self.phase == 4:
            self.phase_4()

    def phase_1(self):
        # Étape 1
        ids_villageois_libres = []
        # Parcourir toutes les tuiles
        for position, data in tuiles.items():
            if "unites" in data and self.player_id in data["unites"]:
                # Vérifier si le joueur possède des villageois (type "v")
                villageois = data["unites"][self.player_id].get("v", {})
                # Ajouter à la liste uniquement les villageois libres
                for villager_id, villager_data in villageois.items():
                    if villager_data.get("Status") == "libre":
                        ids_villageois_libres.append(villager_id)

        for id_unite in ids_villageois_libres
            Recolte_ressources.recolter_ressource_plus_proche_via_trouver(Recolte_ressources.Recolte_ressources, self.player_id, 'v', ids_villageois_libres[0], Recolte_ressources.trouver_plus_proche_ressource(Recolte_ressources.Recolte_ressources, self.player_id, 'v', ids_villageois_libres[0], 'W' ), recolte_max=20)
            Recolte_ressources.recolter_ressource_plus_proche_via_trouver(Recolte_ressources.Recolte_ressources, self.player_id, 'v', ids_villageois_libres[1], Recolte_ressources.trouver_plus_proche_ressource(Recolte_ressources.Recolte_ressources, self.player_id, 'v', ids_villageois_libres[1], 'W' ), recolte_max=20)
            Recolte_ressources.recolter_ressource_plus_proche_via_trouver(Recolte_ressources.Recolte_ressources, self.player_id, 'v', ids_villageois_libres[2], Recolte_ressources.trouver_plus_proche_ressource(Recolte_ressources.Recolte_ressources, self.player_id, 'v', ids_villageois_libres[2], 'G' ), recolte_max=20)

        """        Unit.creation_unite('v', self.player_id)  # Former un villageois
        Buildings.assign_villagers_to_construction(self.player_id)
        Buildings.ajouter_batiment(self.player_id, 'H', x, y, taille, tuiles, status)
        Buildings.creation_batiments(self.player_id, 'H', x, y, taille, tuiles)
        Buildings.assign_villagers_to_construction(self.player_id)
        Buildings.ajouter_batiment(self.player_id, 'C', x, y, taille, tuiles, status)
        Buildings.creation_batiments(self.player_id, 'C', x, y, taille, tuiles)
        self.phase += 1

 def phase_2(self):
        # Étape 2
        current_villagers = len(self.get_villagers())
        if current_villagers < 8:  # Former 4 villageois supplémentaires
            self.create_unit('v')
        else:
            self.assign_villagers_to_resources({'f': 2, 'G': 2})  # 2 nourriture, 2 or

            # Construire une caserne et entraîner des soldats
            if not self.has_building('barracks') and self.can_build_at(self.get_building_site('barracks')):
                self.build_barracks()

            if self.has_building('barracks'):
                self.train_units('s', 2)  # Former 2 swordsmen
                self.build_keep('town_center')  # Construire un keep près du town center
                self.phase += 1  # Passer à l'étape suivante

    def phase_3(self):
        # Étape 3
        self.train_units('a', 3)  # Ajouter 2-3 archers
        self.train_units('s', 2)  # Maintenir une force de swordsmen

        # Construire un deuxième keep si nécessaire
        if self.can_build_keep('resources'):
            self.build_keep('resources')

        # Répartition optimale des ressources
        self.assign_villagers_to_resources({'f': 4, 'W': 4, 'G': 3})

        self.phase += 1  # Passer à l'étape suivante

    def phase_4(self):
        # Étape 4
        if not self.has_building('town_center', count=2):
            if self.can_build_towncenter():
                self.build_towncenter()
                self.build_keep('new_town_center')  # Protéger le nouveau town center

        # Renforcer les défenses
        self.train_units('a', 5)  # 5 archers
        self.train_units('s', 5)  # 5 swordsmen
        self.train_units('h', 3)  # 3 horsemen

        # Construire des bâtiments défensifs
        self.build_keep('strategic_points')

        # Distribution idéale des ressources
        self.assign_villagers_to_resources({'f': 40, 'W': 30, 'G': 30})


