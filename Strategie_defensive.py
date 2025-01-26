from Villager import Villager
from Buildings import Buildings
from Recolte_ressources import Recolte_ressources
from Units import *
from TileMap import TileMap
from constants import *
from Initialisation_Compteur import Initialisation_Compteur


class StrategyManager:
    def __init__(self, gameObj, joueur):
        self.joueur = joueur
        self.gameObj = gameObj
        self.ressource_collector = Recolte_ressources()
        self.unit = Unit()
        self.batiments = self.gameObj.compteurs_joueurs[joueur]["batiments"]
        self.ressources = self.gameObj.compteurs_joueurs[joueur]["ressources"]

    def select_strategy(self):
        """
        Sélectionne dynamiquement la stratégie en fonction des conditions du jeu.
        :return: Stratégie à adopter ('offensive', 'defensive', 'economic')
        """
        # Evaluation des ressources
        gold = self.ressources.get('G', 0)
        wood = self.ressources.get('W', 0)
        food = self.ressources.get('F', 0)
        population = self.ressources.get('max_pop', 0)

        # Analyse des bâtiments militaires
        barracks = self.batiments.get('B', 0)
        archery_range = self.batiments.get('A', 0)
        stable = self.batiments.get('S', 0)

        # Sélection de la stratégie en fonction des conditions
        if gold < 150 and wood < 150 and food < 150:
            # Si on a peu de ressources, stratégie économique
            return 'economic'

        if barracks == 0 and archery_range == 0 and stable == 0:
            # Si aucune infrastructure militaire, on adopte une stratégie économique
            return 'economic'

        if population > 150:
            # Si la base économique est forte, prêt pour l'attaque
            return 'offensive'

        if len(self.find_nearby_enemies()) > 2:
            # Si plusieurs ennemis sont proches, stratégie défensive
            return 'defensive'

        if gold > 300 and wood > 300 and food > 400:
            # Si on a beaucoup de ressources, stratégie offensive
            return 'boom'

        # Par défaut, retour à une stratégie économique
        return 'economic'

    def find_nearby_enemies(self):
        """
        Trouve les ennemis proches du joueur.
        :return: Liste des positions des ennemis proches
        """
        nearby_enemies = []
        for position, tile_data in self.gameObj.tuiles.items():
            if 'unites' in tile_data:
                for enemy, units in tile_data['unites'].items():
                    if enemy != self.joueur:
                        nearby_enemies.append(position)
            if 'batiments' in tile_data:
                for enemy, buildings in tile_data['batiments'].items():
                    if enemy != self.joueur:
                        nearby_enemies.append(position)
        return nearby_enemies

    def execute_strategy(self):
        """
        Exécute la stratégie sélectionnée.
        """
        strategy = self.select_strategy()

        if strategy == 'offensive':
            self.Strat_offensive()
        elif strategy == 'defensive':
            self.Strat_defensive()
        elif strategy == 'economic':
            self.Strat_economique()

    def Strat_offensive(self):
        """
        Exécute la stratégie offensive.
        """
        print("Exécution de la stratégie offensive.")
        # Priorité : Construire des bâtiments militaires, entraîner des unités de combat
        strat_offensive = StratOffensive(self.gameObj, self.joueur)
        strat_offensive.execute(self.joueur)

    def Strat_defensive(self):
        """
        Exécute la stratégie défensive.
        """
        print("Exécution de la stratégie défensive.")
        # Priorité : Construire des bâtiments défensifs, protéger les ressources
        strat_defensive = StratDefensive(self.gameObj, self.joueur)
        strat_defensive.execute(self.joueur)

    def Strat_economique(self):
        """
        Exécute la stratégie économique.
        """
        print("Exécution de la stratégie économique.")
        # Priorité : Augmenter la collecte de ressources, construire des bâtiments économiques
        strat_economique = StratEconomique(self.gameObj, self.joueur)
        strat_economique.execute(self.joueur)


class StratDefensive:
    def __init__(self, gameObj, joueur):
        """
        Initialise la stratégie défensive pour un joueur
        :param gameObj: Objet de jeu contenant l'état global
        :param joueur: Identifiant du joueur
        """
        self.joueur = joueur
        self.gameObj = gameObj
        self.ressource_collector = Recolte_ressources()
        self.unit = Unit()
        self.batiments = self.gameObj.compteurs_joueurs[joueur]["batiments"]
        self.ressources = self.gameObj.compteurs_joueurs[joueur]["ressources"]

    def construire_batiment_defensif(self):
        """
        Construit des bâtiments défensifs comme des murailles, des tours ou des fortifications.
        """
        # Vérifier si les ressources nécessaires sont disponibles pour construire un bâtiment défensif
        gold = self.ressources.get('G', 0)
        wood = self.ressources.get('W', 0)

        if gold > 100 and wood > 200:
            # Logique de construction d'un bâtiment défensif
            self.gameObj.creation_batiments(self.joueur, 'K')
            self.ressources['G'] -= 125  # Déduire le coût en or
            self.ressources['W'] -= 35  # Déduire le coût en bois

    def proteger_ressources(self):
        """
        Déplace les unités militaires pour protéger les ressources
        """
        # Exemple : Déplacer une unité militaire vers les ressources
        for position, tuile in self.gameObj.tuiles.items():
            if 'ressources' in tuile and tuile['ressources']:
                for ressource in tuile['ressources']:
                    if ressource == 'G' or ressource == 'W':  # Par exemple, on protège l'or et le bois
                        print(f"{self.joueur} déplace une unité militaire pour protéger les ressources à {position}")
                        # Logique pour déplacer une unité militaire vers la ressource
                        self.unit.deplacer_unite(self.joueur, 'militaire', 1, position)  # ID de l'unité militaire 1

    def execute(self, joueur):
        """
        Exécute la stratégie défensive
        """
        print("Exécution de la stratégie défensive.")
        # Priorité : Construire des bâtiments défensifs, protéger les ressources
        self.construire_batiment_defensif()
        self.proteger_ressources()


class StratEconomique:
    def __init__(self, gameObj, joueur):
        """
        Initialise la stratégie économique pour un joueur
        :param gameObj: Objet de jeu contenant l'état global
        :param joueur: Identifiant du joueur
        """
        self.joueur = joueur
        self.gameObj = gameObj
        self.ressource_collector = Recolte_ressources()
        self.unit = Unit()
        self.building = Buildings()
        self.batiments = self.gameObj.compteurs_joueurs[joueur]["batiments"]
        self.ressources = self.gameObj.compteurs_joueurs[joueur]["ressources"]

    def construire_batiment_economique(self):
        """
        Construit des bâtiments économiques comme des centres-villes, des fermes, etc.
        """
        self.building.creation_batiments(self.joueur, 'F', )

    def optimiser_collecte_ressources(self):
        """
        Assigne des villageois à la collecte optimale de ressources
        """
        # Exemple de logique d'assignation des villageois
        gold = self.ressources.get('G', 0)
        wood = self.ressources.get('W', 0)

        villageois_inactifs = self.unit.villageois_inactifs(self.joueur)

        if gold < wood:
            ressource = 'G'
            ressource2 = 'W'
        else:
            ressource = 'W'
            ressource2 = 'G'

        taille = len(villageois_inactifs)
        indice_separation = (3*taille) // 4

        for villageois in villageois_inactifs[:indice_separation]:
            posress = self.ressource_collector.trouver_plus_proche_ressource(self.joueur, 'v', villageois, ressource)
            self.unit.deplacer_unite(self.joueur, 'v', villageois, posress)
            if self.unit.verifier_presence_villageois(self.joueur, 'v', villageois, posress):
                self.ressource_collector.recolter_ressource_plus_proche_via_trouver(self.joueur, 'v', villageois, posress)

        for villageois in villageois_inactifs[indice_separation:]:
            posress = self.ressource_collector.trouver_plus_proche_ressource(self.joueur, 'v', villageois, ressource2)
            self.unit.deplacer_unite(self.joueur, 'v', villageois, posress)
            if self.unit.verifier_presence_villageois(self.joueur, 'v', villageois, posress):
                self.ressource_collector.recolter_ressource_plus_proche_via_trouver(self.joueur, 'v', villageois,
                                                                                    posress)


    def execute(self, joueur):
        """
        Exécute la stratégie économique
        """
        food = self.ressources.get('F', 0)

        if food < 50:
            self.construire_batiment_economique()

        self.optimiser_collecte_ressources()


class StratOffensive:
    def __init__(self, gameObj, joueur):
        """
        Initialise la stratégie offensive pour un joueur.
        :param gameObj: Objet de jeu contenant l'état global.
        :param joueur: Identifiant du joueur.
        """
        self.joueur = joueur
        self.gameObj = gameObj
        self.ressource_collector = Recolte_ressources()
        self.unit = Unit()
        self.batiments = self.gameObj.compteurs_joueurs[joueur]["batiments"]
        self.ressources = self.gameObj.compteurs_joueurs[joueur]["ressources"]

    def construire_batiment_militaire(self):
        """
        Construit des bâtiments militaires comme des casernes, des écuries, etc.
        """
        gold = self.ressources.get('G', 0)
        wood = self.ressources.get('W', 0)

        if gold > 300 and wood > 200:
            print(f"{self.joueur} construit une caserne.")
            self.gameObj.construire_batiment(self.joueur, 'caserne')
            self.ressources['G'] -= 300
            self.ressources['W'] -= 200

    def entrainer_unites(self):
        """
        Entraîne des unités militaires.
        """
        food = self.ressources.get('F', 0)
        if food > 100:
            print(f"{self.joueur} entraîne des unités militaires.")
            self.unit.creer_unite(self.joueur, 'militaire')
            self.ressources['F'] -= 100

    def attaquer(self, cible):
        """
        Lance une attaque sur un adversaire.
        :param cible: Identifiant du joueur cible.
        """
        # Logique d'attaque (exemple)
        self.unit.attaquer(self.joueur, cible)

    def execute(self, joueur):
        """
        Exécute la stratégie offensive.
        """
        print("Exécution de la stratégie offensive.")
        self.construire_batiment_militaire()
        self.entrainer_unites()