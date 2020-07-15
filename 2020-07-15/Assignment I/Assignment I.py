# 6201012630037
# Assignment I
# Lauch a pygame window which create 10 non-overlapping / random sizes and colors circles that pop when clicked. 
import pygame 
from random import randint
import math

# Run PyGame
pygame.init()

# set window title
pygame.display.set_caption('Assignment 1') 

# create a clock
clock = pygame.time.Clock()

# Set up screen size 
wide = 800
height = 600
screen  = pygame.display.set_mode((wide, height))

# create a new surface 
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

# create a Circle class
class Circle():
    def __init__(self):
        self.x = randint(0,wide)
        self.y = randint(0,height)
        self.radius = randint(10,20)
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.alpha = randint(200,255)
        self.color = (self.R,self.B,self.G,self.alpha)
    
    def create(self):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        pygame.display.update()
    
    def delete(self):
        pygame.draw.circle(surface, (255,255,255), (self.x, self.y), self.radius)
        pygame.display.update()

# Find cursor in circle
def isInside(circle_x, circle_y, radius, x, y): 
      
    if ((x - circle_x) * (x - circle_x) + 
        (y - circle_y) * (y - circle_y) <= radius**2): 
        return True
    else: 
        return False

def isBiggest(target, all):
    b_count = 0
    for k in all:
        if target != k:
            if target.radius > k.radius:
                b_count+=1
            elif target.radius == k.radius:
                b_count+=1
    if b_count == len(all) - 1:
        return True
    else:
        return False
    

circlelist = []
drawn_c = []
running = True
i = 0
count = 0
# Main code
while running:

    clock.tick( 10 ) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for n in drawn_c:
                if isInside(n.x, n.y, n.radius, mouse_pos[0], mouse_pos[1]):
                    if isBiggest(n, drawn_c):
                        n.delete()
                        drawn_c.remove(n)

    while count < 10:
        circlelist.append('c'+str(i))
        circlelist[i] = Circle()
        draw = True
        
        for j in range(len(circlelist)):
            #check all circle class
            if i != j:
                dist = int(math.hypot(circlelist[i].x - circlelist[j].x, circlelist[i].y - circlelist[j].y))
                #if circle overlaped        
                if dist < int(circlelist[i].radius+circlelist[j].radius):
                    draw = False
            
        if draw:
            circlelist[j].create()
            drawn_c.append(circlelist[j])
            count+=1
        i+=1
            
    # fill the screen with the white color
    screen.fill((255,255,255))
    # draw the surface on the screen
    screen.blit(surface, (0,0))
    pygame.display.update()

pygame.quit()
print(count)
