import pickle
import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import pygame

class Save_and_load:
    def __init__(self):
        pass

    def sauvegarder_jeu(self, tuiles, compteurs_unites, dossier_sauvegarde="sauvegardes"):
        try:
            # Crée le dossier si nécessaire
            if not os.path.exists(dossier_sauvegarde):
                os.makedirs(dossier_sauvegarde)

            # Générer un nom de fichier unique basé sur l'heure actuelle
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            fichier_sauvegarde = os.path.join(dossier_sauvegarde, f"sauvegarde_{timestamp}.pkl")

            # Filtrer les objets pygame.Surface des tuiles
            tuiles_filtered = self._filtrer_surfaces(tuiles)

            # Préparer les données à sauvegarder
            data = {
                "tuiles": tuiles_filtered,
                "compteurs_unites": compteurs_unites
            }

            # Sauvegarder dans un fichier avec pickle
            with open(fichier_sauvegarde, "wb") as fichier:
                pickle.dump(data, fichier)

            print(f"Jeu sauvegardé avec succès dans {fichier_sauvegarde}.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def charger_jeu(self, fichier_sauvegarde):
        try:
            with open(fichier_sauvegarde, "rb") as fichier:
                data = pickle.load(fichier)

            tuiles = data.get("tuiles", {})
            compteurs_unites = data.get("compteurs_unites", {})

            # Re-créer les surfaces à partir des données
            tuiles_recreated = self._recreer_surfaces(tuiles)

            print(f"Jeu chargé avec succès depuis {fichier_sauvegarde}.")
            return tuiles_recreated, compteurs_unites
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
            return None, None

    def choisir_fichier_sauvegarde(self, dossier_sauvegarde="sauvegardes"):
        try:
            # Crée une fenêtre Tkinter minimale
            root = tk.Tk()
            root.withdraw()  # Masque la fenêtre principale

            # Définit le répertoire par défaut et filtre les fichiers .pkl
            fichier = filedialog.askopenfilename(
                initialdir=dossier_sauvegarde,
                title="Choisir une sauvegarde",
                filetypes=(("Fichiers Pickle", "*.pkl"), ("Tous les fichiers", "*.*"))
            )
            return fichier if fichier else None
        except Exception as e:
            print(f"Erreur lors de la sélection : {e}")
            return None

    def _filtrer_surfaces(self, tuiles):
        """
        Filtre les objets pygame.Surface des tuiles, les remplace par des données simples.
        """
        tuiles_filtered = {}
        for coord, data in tuiles.items():
            if isinstance(data, pygame.Surface):
                tuiles_filtered[coord] = {'type': 'surface', 'width': data.get_width(), 'height': data.get_height()}
            else:
                tuiles_filtered[coord] = data
        return tuiles_filtered

    def _recreer_surfaces(self, tuiles):
        """
        Recrée les objets pygame.Surface à partir des données filtrées.
        """
        tuiles_recreated = {}
        for coord, data in tuiles.items():
            if isinstance(data, dict) and data.get('type') == 'surface':
                # Re-créer la surface avec les dimensions sauvegardées
                width = data.get('width', 0)
                height = data.get('height', 0)
                tuiles_recreated[coord] = pygame.Surface((width, height))  # Créer une surface vide, ajouter du contenu selon le besoin
            else:
                tuiles_recreated[coord] = data
        return tuiles_recreated
