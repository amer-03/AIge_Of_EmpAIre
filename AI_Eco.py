from Units import Unit
from Buildings import Buildings
from Recolte_ressources import Recolte_ressources
from constants import builds_dict  # Add this import

class AI_Eco:
    def __init__(self, player_id, game):
        self.player_id = f"joueur_{player_id}"
        self.game = game
        self.state = "BOOM"
        self.min_villagers = 10
        self.min_soldiers = 5
        self.villager_tasks = {}  # Track what each villager is doing

    def get_villager_count(self):
        """Count current villagers"""
        return self.game.compteur[self.player_id]['unites'].get('v', 0)

    def get_idle_villagers(self):
        """Find all idle villagers"""
        idle_villagers = []
        for pos, data in self.game.tiles.items():
            if 'unites' in data and self.player_id in data['unites']:
                villagers = data['unites'][self.player_id].get('v', {})
                for v_id, v_data in villagers.items():
                    if v_data.get('Status') == 'libre':
                        idle_villagers.append(v_id)
        return idle_villagers

    def get_most_needed_resource(self):
        """Determine which resource is most needed using correct keys"""
        resources = self.game.compteur[self.player_id]['ressources']
        
        # Debug resources
        print(f"Current resources: {resources}")
        
        thresholds = {
            'W': 100,
            'G': 100, 
            'F': 100
        }
        
        for res, threshold in thresholds.items():
            if resources.get(res, 0) < threshold:
                return res
                
        return 'W'  # Default to wood if all resources above threshold

    def find_nearest_resource(self, resource_type):
        """Find closest resource of given type"""
        return self.game.recolte.trouver_plus_proche_ressource(
            self.player_id, 'v', 0, resource_type
        )

    def train_villager(self):
        """Create new villager if possible"""
        return self.game.unit.creation_unite('v', self.player_id)

    def can_afford_building(self, building_type):
        """Check if we can afford building with proper resource keys"""
        costs = builds_dict[building_type]['cout']
        resources = self.game.compteur[self.player_id]['ressources']
        
        # Debug print
        print(f"Checking resources: {resources}")
        print(f"Building costs: {costs}")
        
        return all(
            resources.get(resource, 0) >= cost 
            for resource, cost in costs.items()
        )

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
        """Enhanced economic focused strategy with error handling"""
        try:
            # Check villager count
            current_villagers = self.get_villager_count()
            if current_villagers < self.min_villagers:
                return self.train_villager()
                
            # Count existing town centers
            tc_count = 0
            for pos, data in self.game.tiles.items():
                if 'batiments' in data and self.player_id in data['batiments']:
                    if 'T' in data['batiments'][self.player_id]:
                        if data['batiments'][self.player_id]['T'].get('principal', False):
                            tc_count += 1

            # Build town center if possible
            if tc_count < 3 and self.can_afford_building('T'):
                # Find position for new TC
                for x in range(-20, 20):
                    for y in range(-20, 20):
                        if self.is_valid_build_location((x, y)):
                            self.game.buildings.ajouter_batiment(
                                self.player_id, 'T', x, y, 4, self.game.tiles, 1
                            )
                            return True

            # Assign idle villagers to resources
            idle_villagers = self.get_idle_villagers()
            for v_id in idle_villagers:
                needed_resource = self.get_most_needed_resource()
                if resource_pos := self.find_nearest_resource(needed_resource):
                    self.assign_villager_to_resource(v_id, resource_pos)
                    
        except Exception as e:
            print(f"Error in boom strategy: {e}")
            return False

    def is_valid_build_location(self, pos):
        """Check if position is valid for building"""
        x, y = pos
        if pos not in self.game.tiles:
            return True
        return not ('batiments' in self.game.tiles[pos] or 
                   'unites' in self.game.tiles[pos] or 
                   'ressources' in self.game.tiles[pos])

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
    
    def assign_villager_to_resource(self, villager_id, resource_pos):
        """Assign villager to gather resource"""
        for pos, data in self.game.tiles.items():
            if ('unites' in data and 
                self.player_id in data['unites'] and 
                'v' in data['unites'][self.player_id] and 
                villager_id in data['unites'][self.player_id]['v']):
                
                self.game.unit.deplacer_unite(
                    self.player_id, 'v', villager_id, resource_pos
                )
                return True
        return False

    def assign_villager_to_task(self, villager_id, current_pos):
        # First try to find nearby resources
        resource_pos = self.game.recolte.trouver_plus_proche_ressource(
            self.player_id, 'v', villager_id, ressource='W'
        )
        
        if resource_pos:
            # Move to resource
            self.game.unit.deplacer_unite(self.player_id, 'v', villager_id, resource_pos)
            self.villager_tasks[villager_id] = {
                'task': 'gathering',
                'resource': 'W',
                'position': resource_pos
            }
            
            # Set up automatic resource dropoff when full
            if self.game.tiles[current_pos]['unites'][self.player_id]['v'][villager_id]['capacite'] >= 20:
                tc_pos = self.game.recolte.trouver_plus_proche_batiment(self.player_id, 'v', villager_id)
                if tc_pos:
                    self.game.unit.deplacer_unite(self.player_id, 'v', villager_id, tc_pos)
    
    def build_towncenter(self):
        # Check resources
        if (self.game.compteur[self.player_id]['ressources']['W'] >= 350 and 
            len(self.game.buildings.batiments.get(self.player_id, {}).get('T', [])) < 3):
            
            # Find suitable position
            for x in range(-10, 11):
                for y in range(-10, 11):
                    pos = (x, y)
                    if self.can_build_at(pos):
                        self.game.buildings.ajouter_batiment(self.player_id, 'T', x, y, 4, self.game.tiles, 1)
                        return True
        return False
    
    def can_build_at(self, pos):
        return pos in self.game.tiles and not self.game.tiles[pos].get('building')

    def manage_resources(self):
        """Better resource management"""
        resources = self.game.compteur[self.player_id]['ressources']
        
        # Balance gatherers
        if resources['W'] < 100:
            self.reassign_villagers_to('W', 3)
        elif resources['G'] < 100:
            self.reassign_villagers_to('G', 2)
        elif resources['f'] < 100:
            self.reassign_villagers_to('f', 2)
