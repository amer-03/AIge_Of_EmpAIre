class Game :
    def __init__(self, name : str, players : list, game_map, game_time : int = 0):
    #j'ai fixé le temps à 0 je savais pas quoi en faire"""
        self.name = name 
        self.players = players
        self.map = game_map
        self.game_time = game_time
        self.if_running = False
    def start_game(self):
        if self.is_running:
            print("Le jeu '{self.name}' est déjà en route.")
        elif self.is_running == True: 
            print ("Le jeu '{self.name}' a commencé.")
    def pause_game(self):
        if self.is_running:
            self.is_running = False
            print ("Le jeu '{self.name}' est en pause.")
        else: 
            print ("Le jeu '{self.name}' est déjà en pause.")
    def end_game(self):
        if self.is_running:
            self.is_running = False
        print("Le jeu '{self.name}' est terminé. Vous avez joué {self.game_time} minutes.")