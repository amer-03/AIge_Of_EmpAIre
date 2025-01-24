from Villager import Villager
from Buildings import Buildings
from Units import Units
from Recolte_ressources import Recolte_ressources
from TileMap import TileMap
from constants import *
from Initialisation_Compteur import Initialisation_Compteur

class StratOffensive:
    def __init__(self, game_state, joueur):
        self.joueur = joueur
        """
        Initialise une IA simple pour un villageois avec la gestion des tuiles.
        :param game_state: État du jeu contenant les informations sur les unités, ressources, bâtiments, etc.
        """
        self.game_state = game_state
        self.resource_collector = Recolte_ressources()

    def getStatus(self, position, joueur, type_unit, id):
        return (tuiles[position]['unites'][joueur][type_unit][id]['Status'] == 'libre')

    def execute(self, joueur):
        """from Game import Game

        
        #Exécute la logique de l'IA pour tous les villageois d'un joueur.
        #Si un villageois est inactif, il collecte du bois.
        
        for position, tuile in tuiles.items():
            # Vérifier s'il y a des unités du joueur sur cette tuile
            if 'unites' in tuile and joueur in tuile['unites']:
                unites_joueur = tuile['unites'][joueur]
                for type_unit, unites in unites_joueur.items():
                    if type_unit == 'v':  # Vérifier que c'est une unité villageoise
                        
                        for id_unite, details_unite in unites.items():
                            # Vérifier le statut de l'unité
                            status = self.getStatus(position, joueur, type_unit, id_unite)
                            if status == False:  # Si l'unité est inactive
                                print ("for")
                                # Trouver la position de la ressource la plus proche
                                print ("ressources")
                                pos_bois = self.resource_collector.trouver_plus_proche_ressource(
                                    joueur, type_unit, id_unite, "W"
                                )
                                if pos_bois:
                                    # Déplacer l'unité vers la ressource
                                    self.resource_collector.unit.deplacer_unite(joueur, type_unit, id_unite, pos_bois)
                                    # Collecter la ressource une fois arrivée
                                    self.resource_collector.recolter_ressource_plus_proche_via_trouver(
                                        joueur, type_unit, id_unite, posress=pos_bois
                                    )
                                else:
                                    print(f"Aucune ressource bois disponible pour l'unité {id_unite}.") """
        from Game import Game

        """
        Exécute la logique de l'IA pour tous les villageois d'un joueur.
        Si un villageois est inactif, il collecte du bois.
        """
        villageois_inactifs = []

        for position, tuile in tuiles.items():
            # Vérifier s'il y a des unités du joueur sur cette tuile
            if 'unites' in tuile and joueur in tuile['unites']:
                unites_joueur = tuile['unites'][joueur]
                for type_unit, unites in unites_joueur.items():
                    if type_unit == 'v':  # Vérifier que c'est une unité villageoise
                        for id_unite, details_unite in unites.items():
                            # Vérifier le statut de l'unité
                            status = self.getStatus(position, joueur, type_unit, id_unite)
                            if status == True:  # Si l'unité est inactive
                                villageois_inactifs.append((position, joueur, type_unit, id_unite))

        # Traiter les villageois inactifs
        for id_unite in villageois_inactifs:
            # Trouver la position de la ressource la plus proche
            pos_bois = self.resource_collector.trouver_plus_proche_ressource(position, joueur, type_unit, id_unite, "W")
            print("haha")
            if pos_bois:
                # Déplacer l'unité vers la ressource
                self.resource_collector.unit.deplacer_unite(position, joueur, type_unit, id_unite, pos_bois)
                # Collecter la ressource une fois arrivée
                self.resource_collector.recolter_ressource_plus_proche_via_trouver(joueur, type_unit, id_unite, posress=pos_bois)
            else:
                print(f"Aucune ressource bois disponible pour l'unité {id_unite}.")
