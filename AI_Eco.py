from Units import Units
from Buildings import Buildings
from Recolte_ressources import Recolte_ressources
from constants import builds_dict, action_a_executer  # Add action_a_executer import

class AI_Eco:
    def __init__(self, gameObj, joueur):
        self.joueur = joueur
        self.gameObj = gameObj
        self.ressource_collector = Recolte_ressources(gameObj)
        self.unit = self.gameObj.unit
        self.state = "BOOM"
        self.min_villagers = 10
        self.min_soldiers = 5

    def update(self):
        if self.state == "BOOM":
            self.execute_boom_strategy()
        else:
            self.execute_defense_strategy()

    def execute_boom_strategy(self):
        try:
            current_villagers = self.get_villager_count()
            if current_villagers < self.min_villagers:
                return self.train_villager()

            idle_villagers = self.get_idle_villagers()
            for v_id in idle_villagers:
                needed_resource = self.get_most_needed_resource()
                if resource_pos := self.find_nearest_resource(needed_resource):
                    self.assign_villager_to_resource(v_id, resource_pos)

            tc_count = sum(
                1 for pos, data in self.gameObj.tuiles.items()
                if 'batiments' in data and self.joueur in data['batiments'] and 'T' in data['batiments'][self.joueur]
            )

            if tc_count < 3 and self.can_afford_building('T'):
                for x in range(-20, 20):
                    for y in range(-20, 20):
                        if self.is_valid_build_location((x, y)):
                            self.gameObj.buildings.ajouter_batiment(self.joueur, 'T', x, y, 4, self.gameObj.tuiles, 1)
                            return True

        except Exception as e:
            print(f"Error in boom strategy: {e}")
            return False

    def execute_defense_strategy(self):
        current_soldiers = self.get_soldier_count()
        if current_soldiers < self.min_soldiers:
            self.create_unit('s')

    def get_villager_count(self):
        return self.gameObj.compteur[self.joueur]['unites'].get('v', 0)

    def get_idle_villagers(self):
        idle_villagers = []
        for pos, data in self.gameObj.tuiles.items():
            if 'unites' in data and self.joueur in data['unites']:
                villagers = data['unites'][self.joueur].get('v', {})
                for v_id, v_data in villagers.items():
                    if v_data['Status'] == 'libre':
                        idle_villagers.append(v_id)
        return idle_villagers

    def get_most_needed_resource(self):
        resources = self.gameObj.compteur[self.joueur]['ressources']
        thresholds = {'W': 100, 'G': 100, 'F': 100}
        for res, threshold in thresholds.items():
            if resources.get(res, 0) < threshold:
                return res
        return 'W'

    def find_nearest_resource(self, resource_type):
        return self.ressource_collector.trouver_plus_proche_ressource(self.joueur, 'v', 0, resource_type)

    def train_villager(self):
        return self.unit.creation_unite('v', self.joueur)

    def can_afford_building(self, building_type):
        costs = builds_dict[building_type]['cout']
        resources = self.gameObj.compteur[self.joueur]['ressources']
        return all(resources.get(r, 0) >= c for r, c in costs.items())

    def is_valid_build_location(self, pos):
        x, y = pos
        if pos not in self.gameObj.tuiles:
            return True
        return not ('batiments' in self.gameObj.tuiles[pos] or 'unites' in self.gameObj.tuiles[pos] or 'ressources' in self.gameObj.tuiles[pos])

    def create_unit(self, unit_type):
        costs = self.unit.units_dict[unit_type]['cout']
        resources = self.gameObj.compteur[self.joueur]['ressources']
        if all(resources.get(r, 0) >= c for r, c in costs.items()):
            self.unit.creation_unite(unit_type, self.joueur)

    def assign_villager_to_resource(self, villager_id, resource_pos):
        for pos, data in self.gameObj.tuiles.items():
            if 'unites' in data and self.joueur in data['unites'] and 'v' in data['unites'][self.joueur] and villager_id in data['unites'][self.joueur]['v']:
                self.unit.deplacer_unite(self.joueur, 'v', villager_id, resource_pos)
                return True
        return False

    def get_soldier_count(self):
        return self.gameObj.compteur[self.joueur]['unites'].get('s', 0) + self.gameObj.compteur[self.joueur]['unites'].get('a', 0)

    def getStatus(self, position, joueur, type_unit, id):
        return (self.gameObj.tuiles[position]['unites'][joueur][type_unit][id]['Status'] == 'libre')

    def execute(self, joueur):
        villageois_inactifs = []

        # Find idle villagers
        for position, tuile in self.gameObj.tuiles.items():
            if 'unites' in tuile and joueur in tuile['unites']:
                unites_joueur = tuile['unites'][joueur]
                for type_unit, unites in unites_joueur.items():
                    if type_unit == 'v':
                        for id_unite, details_unite in unites.items():
                            if self.getStatus(position, joueur, type_unit, id_unite):
                                villageois_inactifs.append((position, joueur, type_unit, id_unite))

        # Process idle villagers
        for i in villageois_inactifs:
            position_unite = i[0]
            joueur = i[1] 
            type_unit = i[2]
            id_unite = i[3]

            pos_bois = self.ressource_collector.trouver_plus_proche_ressource(position_unite, joueur, type_unit, id_unite, "W")
            if pos_bois:
                self.unit.deplacer_unite(joueur, type_unit, id_unite, pos_bois)
                action_a_executer.append(
                    lambda posress=pos_bois: self.ressource_collector.recolter_ressource_plus_proche_via_trouver(
                        joueur, type_unit, id_unite, posress=posress
                    )
                )

                def action_apres_deplacement():
                    if int(self.gameObj.tuiles[self.unit.position]['unites'][joueur][type_unit][id_unite]['capacite']) == 20:
                        pos_batiment = self.ressource_collector.trouver_plus_proche_batiment(joueur, type_unit, id_unite)
                        if pos_batiment:
                            self.unit.deplacer_unite(joueur, type_unit, id_unite, pos_batiment)

                action_a_executer.append(action_apres_deplacement)

                def deposer_ressources_in_batiment():
                    quantite = 20
                    ressource = 'f'
                    self.ressource_collector.deposer_ressources(quantite, joueur, type_unit, id_unite, ressource)

                action_a_executer.append(deposer_ressources_in_batiment)