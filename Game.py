import pygame

class Game :
    def __init__(self):
        pygame.init()
        self.name=""
        self.player=player
        self.map=map
        self.game_time=pygame.time.Clock
        self.running = True
        self.screen=pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h),pygame.FULLSCREEN)
    #def start_game(self):
    #    if self.is_running:
    #        print("Le jeu '{self.name}' est déjà en route.")
    #    elif self.is_running == True: 
    #        print ("Le jeu '{self.name}' a commencé.")
    #def pause_game(self):
    #    if self.is_running:
    #        self.is_running = False
    #        print ("Le jeu '{self.name}' est en pause.")
    #    else: 
    #        print ("Le jeu '{self.name}' est déjà en pause.")
    #def end_game(self):
    #    if self.is_running:
    #        self.is_running = False
    #    print("Le jeu '{self.name}' est terminé. Vous avez joué {self.game_time} minutes.")