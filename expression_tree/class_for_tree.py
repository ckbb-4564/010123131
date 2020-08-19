import pygame

class Stack:
    def __init__(self):
        self.stacklist = []
        self.size = 0

    def push(self,item):
        self.stacklist.append(item)
        self.size += 1
    
    def pop(self):
        item = self.stacklist.pop()
        self.size -= 1
        return item

    def top(self):
        item = self.stacklist[-1]
        return item
    
    def is_empty(self):
        state = self.size == 0
        return state

class Expression_Tree:    
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class Circle:
    def __init__(self,x, y, r, text, color = (255,192,203)):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.text = text
    
    def createCircle(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def createText(self):
        font = pygame.font.Font('freesansbold.ttf', self.r*2)
        text_box = font.render(self.text, True, (255,105,180))
        text_rect = text_box.get_rect()
        text_rect.center = (self.x, self.y)
        screen.blit(text_box, text_rect)

class Line:
    def __init__(self, x_start, x_stop, y_start, y_stop, thick):
        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.thick = int(thick)
    
    def createLine(self):
        pygame.draw.line(screen, (255,192,203), (self.x_start, self.y_start), (self.x_stop, self.y_stop), self.thick)