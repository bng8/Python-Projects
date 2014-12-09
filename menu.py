import pygame
import time
import sys

class Menu:
    def __init__(self, handler):
        self.size = (1024,768)
        self.title = pygame.image.load("res/211title.png").convert_alpha()
        self.bgImg = pygame.image.load("res/menubg.png").convert_alpha()
        playIcon = pygame.image.load("res/playicon.png").convert_alpha()
        instructionsIcon = pygame.image.load("res/instructionsicon.png").convert_alpha()
        creditsIcon = pygame.image.load("res/creditsicon.png").convert_alpha()
        self.icon_list = [playIcon, instructionsIcon, creditsIcon]
        pygame.font.init()

        self.handler = handler

        icon_rect_list = []
        x = 0
        for icon in self.icon_list:
            icon_rect = icon.get_rect()
            icon_rect.x,icon_rect.y = (420,450+x)
            icon_rect_list.append(icon_rect)

        self.icon_rect_list = []

        x = 0
        for icon in self.icon_list:
            icon_rect = icon.get_rect()
            icon_rect.x,icon_rect.y = (420,450+x)
            self.icon_rect_list.append(icon_rect)
            x+=100
        
        self.font = pygame.font.SysFont('comicsansms', 16)

        #Imports background music for menu
        pygame.mixer.music.load("res/Menu.wav")
        pygame.mixer.music.play(-1)

    #Used for instructions/credit screen

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.bgImg,(0,0))
        screen.blit(self.title,(335,150))

        for i in range(len(self.icon_list)):
            screen.blit(self.icon_list[i], self.icon_rect_list[i])
        
        for i, icon in enumerate(self.icon_rect_list):
            if icon.collidepoint(pygame.mouse.get_pos()) and i == 0:
                if pygame.mouse.get_pressed()[0]:
                    pygame.mixer.music.fadeout(1500)
                    self.handler.curState = 3
                break

            if icon.collidepoint(pygame.mouse.get_pos()) and i == 1:
                if pygame.mouse.get_pressed()[0]:
                    self.handler.curState = 2
                break

            if icon.collidepoint(pygame.mouse.get_pos()) and i == 2:
                if pygame.mouse.get_pressed()[0]:
                    self.handler.curState = 1
                break

    def update(self):
        pass
            
