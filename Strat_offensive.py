from Villager import Villager
from Buildings import Buildings
from Units import Units
from Recolte_ressources import Recolte_ressources
from TileMap import TileMap
from constants import *
from Initialisation_Compteur import Initialisation_Compteur

class StratOffensive:
    def __init__(self, gameObj, joueur):
        self.joueur = joueur
        """
        Initialise une IA simple pour un villageois avec la gestion des tuiles.
        :param game_state: État du jeu contenant les informations sur les unités, ressources, bâtiments, etc.
        """
        self.gameObj = gameObj
        self.ressource_collector = Recolte_ressources(gameObj)
        self.unit = self.gameObj.unit

    def getStatus(self, position, joueur, type_unit, id):
        return (self.gameObj.tuiles[position]['unites'][joueur][type_unit][id]['Status'] == 'libre')

    
    def bouge(self, joueur, type_unit, id_unite, pos_bois):
        self.unit.deplacer_unite(joueur, type_unit, id_unite, pos_bois)

        
        """action_a_executer.append(
            lambda posress=pos_bois: self.resource_collector.recolter_ressource_plus_proche_via_trouver(joueur, type_unit, id_unite, posress=posress))
        def action_apres_deplacement():
            if int(self.gameObj.tuiles[self.unit.position]['unites'][joueur][type_unit][id_unite]['capacite']) == 20:
                pos_batiment = self.resource_collector.trouver_plus_proche_batiment(joueur, type_unit, id_unite)
                if pos_batiment:
                    self.unit.deplacer_unite(joueur, type_unit, id_unite, pos_batiment)

        action_a_executer.append(action_apres_deplacement)"""

        def deposer_ressources_in_batiment():
                quantite = 20
                ressource = 'f'
                self.resource_collector.deposer_ressources(quantite, joueur, type_unit, id_unite, ressource)

        action_a_executer.append(deposer_ressources_in_batiment)
    
    def execute(self, joueur):
        """from Game import Game

        
        #Exécute la logique de l'IA pour tous les villageois d'un joueur.
        #Si un villageois est inactif, il collecte du bois.
        
        for position, tuile in self.gameObj.tuiles.items():
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
        
        """
        Exécute la logique de l'IA pour tous les villageois d'un joueur.
        Si un villageois est inactif, il collecte du bois.
        """
        tier1 = []
        tier2 = []
        tier3 = []
        for position, tuile in self.gameObj.tuiles.items():
            if 'unites' in tuile and joueur in tuile['unites']:
                unites_joueur = tuile['unites'][joueur]
                for type_unit, unites in unites_joueur.items():
                    if type_unit == 'v':
                        for id_unite, details_unite in unites.items():
                            if self.getStatus(position, joueur, type_unit, id_unite):
                                if id_unite % 3 == 0:
                                    tier1.append((position, joueur, type_unit, id_unite))
                                elif id_unite % 3 == 1:
                                    tier2.append((position, joueur, type_unit, id_unite))
                                elif id_unite % 3 == 2:
                                    tier3.append((position, joueur, type_unit, id_unite))
        if len(tier1) > 0:
            print("tier1", tier1)
        """if tier2:
            print("tier2", tier2)"""
        """if tier3:
            print("tier3", tier3)"""
        # Traiter les villageois inactifs+6
        for (ressource, villagers) in [('W', tier1), ('G', tier2)]:      
            for i in villagers:
                print ("je suis le villageois", i, "du tableau", villagers)
                # Trouver la position de la ressource la plus proche
                id_unite = i[3]
                type_unit = i[2]
                joueur = i[1]
                position_unite = i[0]

                pos_bois = self.ressource_collector.trouver_plus_proche_ressource(position_unite, joueur, type_unit, id, ressource)
                if pos_bois:
                    self.unit.deplacer_unite(joueur, type_unit, id_unite, pos_bois) 
                    action_a_executer.append(
                    lambda posress=pos_bois: self.ressource_collector.recolter_ressource_plus_proche_via_trouver(joueur, type_unit, id_unite, posress=posress))
                    def action_apres_deplacement():
                        pos_batiment = self.ressource_collector.trouver_plus_proche_batiment(joueur, type_unit, id_unite)
                        if pos_batiment:
                            self.unit.deplacer_unite(joueur, type_unit, id_unite, pos_batiment)

                    action_a_executer.append(action_apres_deplacement)

                    def deposer_ressources_in_batiment():
                            quantite = 20
                            self.ressource_collector.deposer_ressources(self.unit.position, quantite, joueur, type_unit, id_unite, ressource)

                    action_a_executer.append(deposer_ressources_in_batiment)
                


        """for j in tier2:
                        # Trouver la position de la ressource la plus proche
            id_unite = j[3]
            type_unit = j[2]
            joueur = j[1]
            position_unite = j[0]

            pos_bois = self.ressource_collector.trouver_plus_proche_ressource(position_unite, joueur, type_unit, id, "G")
            if pos_bois:
                self.unit.deplacer_unite(joueur, type_unit, id_unite, pos_bois) 
                action_a_executer.append(
                lambda posress=pos_bois: self.ressource_collector.recolter_ressource_plus_proche_via_trouver(joueur, type_unit, id_unite, posress=posress))
                def action_apres_deplacement():
                    if int(self.gameObj.tuiles[self.unit.position]['unites'][joueur][type_unit][id_unite]['capacite']) == 20:
                        pos_batiment = self.ressource_collector.trouver_plus_proche_batiment(joueur, type_unit, id_unite)
                        if pos_batiment:
                            self.unit.deplacer_unite(joueur, type_unit, id_unite, pos_batiment)

                action_a_executer.append(action_apres_deplacement)

                def deposer_ressources_in_batiment():
                        quantite = 20
                        ressource = 'G'
                        self.ressource_collector.deposer_ressources(self.unit.position, quantite, joueur, type_unit, id_unite, ressource)

                action_a_executer.append(deposer_ressources_in_batiment)"""
