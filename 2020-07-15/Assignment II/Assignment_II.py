# 6201012630037
#Assignment II
# Lauch a pygame window which create 10 non-overlapping / random sizes and colors circles that pop when clicked. Circles can now moving and bounce to border and each other
import pygame 
from random import *
import math

# Run PyGame
pygame.init()

# set window title
pygame.display.set_caption('Assignment 2')

# create a clock
clock = pygame.time.Clock()

# Set up screen size 
wide = 800
height = 600
screen  = pygame.display.set_mode((wide, height))

# create a Circle class
class Circle():
    def __init__(self):
        self.x = randint(0,wide)
        self.y = randint(0,height)
        self.radius = randint(10,20)
        self.x_speed = choice(move)
        self.y_speed = choice(move)
        self.colli = True

        build = True
        while build:
            self.top = self.y - self.radius
            self.bot = self.y + self.radius
            self.left = self.x - self.radius
            self.right = self.x + self.radius
            self.R = randint(0,255)
            self.G = randint(0,255)
            self.B = randint(0,255)
            self.alpha = randint(200,255)
            self.color = (self.R,self.B,self.G,self.alpha)
            if self.R == 0 or self.G == 0 or self.B == 0 or self.top < 0 or self.bot > height or self.left < 0 or self.right > wide:
                self.x = randint(0,wide)
                self.y = randint(0,height)
                self.radius = randint(10,20)
                self.R = randint(0,255)
                self.G = randint(0,255)
                self.B = randint(0,255)
                continue
            if self.R != 0 or self.G != 0 or self.B != 0 or self.top >= 0 or self.bot <= height or self.left >= 0 or self.right <= wide:
                build = False
                

        
    
    def create(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def delete(self):
        pygame.draw.circle(screen, (255,255,255), (int(self.x), int(self.y)), self.radius)

# Draw circle
def drawCir(cirNum):
    global circlelist, drawn_c
    count = 0
    i = 0
    test = True
    while test:
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
            count += 1
        if count == cirNum:
            test = False
        else:
            i += 1
    return drawn_c
# Find cursor in circle
def isInside(circle_x, circle_y, radius, x, y): 
      
    if ((x - circle_x) * (x - circle_x) + 
        (y - circle_y) * (y - circle_y) <= radius**2): 
        return True
    else: 
        return False
# Find the biggest
def isBiggest(target, all):
    big_count = 0
    for k in all:
        if target != k:
            if target.radius >= k.radius:
                big_count += 1
    if big_count == len(all) - 1:
        return True
    else:
        return False
# Ask that have no circles in pygame window
def noCircles():
    if len(drawn_c) == 0:
        return True
    else:
        return False
# Update circles coordinate
def update(item):
    item.x += item.x_speed
    item.y += item.y_speed
    item.top = item.y - item.radius
    item.bot = item.y + item.radius
    item.left = item.x - item.radius
    item.right = item.x + item.radius
# Circles hit border
def checkColliBorder(item):
    if item.x < item.radius or item.x > wide - item.radius:
        item.x_speed *= -1
    if item.y < item.radius or item.y > height - item.radius:
        item.y_speed *= -1
# Circles hit each other
def checkColliOther(item,other):
    more_dist = math.hypot(item.x - other.x , item.y - other.y)
    sum_r = item.radius + other.radius
    if more_dist - sum_r <= 3:
        # Change circles directions
        itemSpeed = math.sqrt((item.x_speed ** 2) + (item.y_speed ** 2))
        XDiff = - (item.x - other.x)
        YDiff = - (item.y - other.y)
        if XDiff > 0:
            if YDiff > 0:
                Angle = math.degrees(math.atan(YDiff / XDiff))
                XSpeed = - itemSpeed * math.cos(math.radians(Angle))
                YSpeed = - itemSpeed * math.sin(math.radians(Angle))
            elif YDiff < 0:
                Angle = math.degrees(math.atan(YDiff / XDiff))
                XSpeed = - itemSpeed * math.cos(math.radians(Angle))
                YSpeed = - itemSpeed * math.sin(math.radians(Angle))
        elif XDiff < 0:
            if YDiff > 0:
                Angle = 180 + math.degrees(math.atan(YDiff / XDiff))
                XSpeed = - itemSpeed * math.cos(math.radians(Angle))
                YSpeed = - itemSpeed * math.sin(math.radians(Angle))
            elif YDiff < 0:
                Angle = -180 + math.degrees(math.atan(YDiff / XDiff))
                XSpeed = - itemSpeed * math.cos(math.radians(Angle))
                YSpeed = - itemSpeed * math.sin(math.radians(Angle))
        elif XDiff == 0:
            if YDiff > 0:
                Angle = -90
            else:
                Angle = 90
            XSpeed = itemSpeed * math.cos(math.radians(Angle))
            YSpeed = itemSpeed * math.sin(math.radians(Angle))
        elif YDiff == 0:
            if XDiff < 0:
                Angle = 0
            else:
                Angle = 180
            XSpeed = itemSpeed * math.cos(math.radians(Angle))
            YSpeed = itemSpeed * math.sin(math.radians(Angle))
        item.x_speed = XSpeed
        item.y_speed = YSpeed

# Main code
move = [-4,4]
drawn_c = []
circlelist = []
drawn_c = []
cirNum = 10
running = True
drawCir(cirNum)

# Main loop
while running:
    clock.tick( 25 ) 
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
    
    screen.fill((0,0,0))
    
    for a in drawn_c:
        checkColliBorder(a)
        for b in drawn_c:
            if a != b:
                checkColliOther(a,b)
                
    for c in drawn_c:
        update(c)
        c.delete()
        c.create()
        


    pygame.display.flip()

pygame.quit()