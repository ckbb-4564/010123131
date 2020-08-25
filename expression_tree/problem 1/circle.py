#Circle class
import pygame
from pygame.locals import *

class Circle:
    
    def __init__(self,x, y, r, text, screen, color=(255,192,203)):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.text = text
        self.screen = screen
    
    def create_circle(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def create_text(self):
        font = pygame.font.Font('freesansbold.ttf', self.r*2)
        text_box = font.render(self.text, True, (255,105,180))
        text_rect = text_box.get_rect()
        text_rect.center = (self.x, self.y)
        self.screen.blit(text_box, text_rect)