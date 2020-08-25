import pygame
import math
from pygame.locals import *
from circle import Circle
from line import Line

class Draw_Tree:

    def __init__(self, root):
        self.screen = None
        self.screen_width = None
        self.screen_height = None
        self.range_width = None
        self.range_height = None
        self.radius = None
        self.root = root

    def find_depth(self, root):
        if root:
            left = self.find_depth(root.left)
            center = self.find_depth(root.center)
            right = self.find_depth(root.right)
            
            return max(left, center, right) + 1
        
        else:
            return 0

    def set_screen(self, width, height, screen):
        self.screen_width = width
        self.screen_height = height
        self.screen = screen

    def set_scale(self):
        depth = self.find_depth(self.root)
        leaf = 2 ** depth
        self.range_width = self.screen_width // leaf
        self.range_height = self.screen_height // depth
        self.radius = self.range_width
    
    def draw_child(self, text, scale_x, x, y, position):
        if position == 'left':
            angle = 135
            x_stop = x - scale_x
        elif position == 'right':
            angle = 45
            x_stop = x + scale_x
        elif position == 'center':
            angle = 90
            x_stop = x
        y_stop = y + self.range_height

        x_start = x + int((self.radius - self.radius // 4) * math.cos(math.radians(angle)))
        y_start = y + int((self.radius - self.radius // 4) * math.sin(math.radians(angle)))
        line = Line(x_start, x_stop, y_start, y_stop, self.radius // 2, self.screen)
        line.create_line()

        circle = Circle(x_stop, y_stop, self.radius, text, self.screen)
        circle.create_circle()
        circle.create_text()
        
        return x_stop, y_stop
    
    def draw(self, root, scale_x, x = 0, y = 0, position = 'root'):
        
        if type(root) == str:
            text = root.value
            self.draw_child(text, scale_x//2, x, y, position)
        
        elif root:
            text = root.value
            
            if position == 'root':
                x = self.screen_width // 2
                y = self.range_height // 2
                circle = Circle(x, y, self.radius, text, self.screen)
                circle.create_circle()
                circle.create_text()
                
                if text == '!':
                    self.draw(root.center, scale_x, x, y, 'center')
                
                else:
                    self.draw(root.left, scale_x // 2, x, y, 'left')
                    self.draw(root.right, scale_x // 2, x, y, 'right')
            
            elif text == '!':
                x, y = self.draw_child(text, scale_x // 2, x, y, position)
                self.draw(root.center, scale_x, x, y, 'center')
            
            else:
                x, y = self.draw_child(text, scale_x // 2, x, y, position)
                self.draw(root.left, scale_x // 2, x, y, 'left')
                self.draw(root.right, scale_x // 2, x, y, 'right')