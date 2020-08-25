import pygame
from pygame.locals import *

class Line:
    
    def __init__(self, x_start, x_stop, y_start, y_stop, thick, screen, color = (255,192,203)):
        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.thick = int(thick)
        self.screen = screen
        self.color = color
    
    def create_line(self):
        pygame.draw.line(self.screen, self.color, (self.x_start, self.y_start), (self.x_stop, self.y_stop), self.thick)