import pygame
from Map import *
#from Player import *

class Game :
    def __init__(self):
        pygame.init()
        self.name=""
        #self.player=Player
        self.map=Map
        self.game_time=pygame.time.Clock
        self.running = True
        self.screen=pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h),pygame.FULLSCREEN)
    
    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type==pygame.QUIT: self.running=False
                #elif e.type == pygame.KEYDOWN: self.running=False
        
            self.screen.fill((139,69,19))
        
            pygame.display.flip()    

Game().run()  
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