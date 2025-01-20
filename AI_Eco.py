from Units import Unit
from Buildings import Buildings
from Recolte_ressources import Recolte_ressources

class AI_Eco:
    def __init__(self, player_id, game):
        self.player_id = f"joueur_{player_id}"
        self.game = game
        self.state = "BOOM"
        self.min_villagers = 10
        self.min_soldiers = 5

    def update(self):
        if self.is_under_attack():
            self.state = "DEFEND"
        
        if self.state == "BOOM":
            self.execute_boom_strategy()
        else:
            self.execute_defense_strategy()
    
    def is_under_attack(self):
        for pos, data in self.game.tiles.items():
            if 'unites' in data:
                for player, units in data['unites'].items():
                    if player != self.player_id and any(unit in ['s', 'a'] for unit in units.keys()):
                        return True
        return False
    
    def execute_boom_strategy(self):
        # Create villagers continuously
        self.create_unit('v')
        
        # Create Town Centers continuously
        self.build_towncenter()
    
    def execute_defense_strategy(self):
        # Create military units
        current_soldiers = (self.game.compteur[self.player_id]['unites'].get('s', 0) + 
                          self.game.compteur[self.player_id]['unites'].get('a', 0))
        if current_soldiers < self.min_soldiers:
            self.create_unit('s')
    
    def create_unit(self, unit_type):
        costs = self.game.unit.units_dict[unit_type]['cout']
        resources = self.game.compteur[self.player_id]['ressources']
        
        if (resources['W'] >= costs['Wood'] and 
            resources['G'] >= costs['Gold'] and 
            resources['f'] >= costs['Food']):
            self.game.unit.creation_unite(unit_type, self.player_id)
    
    def assign_villagers(self):
        for pos, data in self.game.tiles.items():
            if 'unites' in data and self.player_id in data['unites']:
                villagers = data['unites'][self.player_id].get('v', {})
                for v_id, v_data in villagers.items():
                    if v_data['Status'] == 'libre':
                        self.assign_villager_to_resource(v_id)
    
    def assign_villager_to_resource(self, villager_id):
        resources = ['W', 'G', 'f']
        for resource in resources:
            pos = self.game.recolte.trouver_plus_proche_ressource(
                self.player_id, 'v', villager_id, resource
            )
            if pos:
                self.game.unit.deplacer_unite(self.player_id, 'v', villager_id, pos)
                break
    
    def build_towncenter(self):
        costs = self.game.buildings.builds_dict['T']['cout']
        resources = self.game.compteur[self.player_id]['ressources']
        
        if (resources['W'] >= costs['Wood'] and 
            resources['G'] >= costs['Gold'] and 
            resources['f'] >= costs['Food']):
            # Find suitable position for building
            for x in range(self.game.size):
                for y in range(self.game.size):
                    if self.can_build_at((x, y)):
                        taille = self.game.buildings.builds_dict['T']['taille']
                        self.game.buildings.ajouter_batiment(
                            self.player_id, 'T', x, y, taille, 
                            self.game.tiles, 1
                        )
                        return
    
    def can_build_at(self, pos):
        return pos in self.game.tiles and not self.game.tiles[pos].get('building')
