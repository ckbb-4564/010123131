import pygame
import math
import sys
from pygame.locals import *
#---------------------------This is for Assignment 1 only

# Stack class
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

# Tree class
class Expression_Tree:    
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# Circle class
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

# Line class
class Line:
    def __init__(self, x_start, x_stop, y_start, y_stop, thick):
        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.thick = int(thick)
    
    def createLine(self):
        pygame.draw.line(screen, (255,192,203), (self.x_start, self.y_start), (self.x_stop, self.y_stop), self.thick)

# Start pygame
pygame.init()
# Set screen wide x height = 500 x 500
scr_w, scr_h = 500, 500
screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption('Assignment 1') 

surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

# Convert infixes to postfixes
def infix_to_postfix(infix):
    global number, alphabet, operator, operator_value
    # Create stack
    operator_stack = Stack()
    # Output Here
    postfix = []
    operand = ''
    temp = ''
    
    for item in infix:
        
        if item in alphabet or item in number:
            temp = item
            operand += temp
        
        elif item == ' ':
            continue
        
        else:
            if operand !='':
                postfix.append(operand)
                operand = ''
            
            if item == '(':
                operator_stack.push(item)
            
            elif item == ')':
                token = operator_stack.pop()
                # Pop everything in stack into output until reach (
                while token != '(':
                    postfix.append(token)
                    token = operator_stack.pop()
            
            elif item in operator:
                
                if operator_stack.is_empty():
                    operator_stack.push(item)
                
                else:
                    token = operator_stack.top()
                    # Compare precendence between two operators
                    if operator_value[item] > operator_value[token]:
                        operator_stack.push(item)
                    
                    else:
                        state = True
                        # Compare precendence between two operators
                        while (not operator_stack.is_empty()) and operator_value[item] < operator_value[token] and state:
                            # Pop from stack into output
                            temp = operator_stack.pop()
                            
                            if not operator_stack.is_empty():
                                token = operator_stack.top()
                            
                            else:
                                state = False
                            
                            postfix.append(temp)
                        
                        operator_stack.push(item)
    # Pop from stack into output
    while not operator_stack.is_empty():
        token = operator_stack.pop()
        postfix.append(token)
    
    return postfix

# Convert post fix into linked tree
def create_expression_tree(postfix):
    global number, alphabet, operator
    
    tree_stack = Stack()
    
    for item in postfix:
        
        if item == '!':
            child = tree_stack.pop()
            expression_tree = Expression_Tree(item)
            expression_tree.left = child
            tree_stack.push(expression_tree)
        
        elif item in operator:
            # Make Left/Right child
            right_child = tree_stack.pop()
            left_child = tree_stack.pop()
            expression_tree = Expression_Tree(item)
            expression_tree.left = left_child
            expression_tree.right = right_child
            tree_stack.push(expression_tree)
        
        else:
            expression_tree = Expression_Tree(item)
            tree_stack.push(expression_tree)
    
    exp_tree_output = tree_stack.pop()
    return exp_tree_output

# Preorder travesal
def preOrder(root):
    return ([root.value] + preOrder(root.left) + preOrder(root.right)) if root else []

# Find tree's depth
def findDepth(root):
    if root:
        
        left = findDepth(root.left)
        right = findDepth(root.right)
        return max(left, right) + 1
    
    else:
        return 0
    
# Find scales for draw a tree   
def screenScale(root, scr_w, scr_h):
    global operator
    
    depth = findDepth(root)
    leaf = 2 ** depth
    # range wide and height
    rw = scr_w // leaf
    rh = scr_h // depth
    #radius
    r = rw
    
    return rw, rh, r

# Left/Right child then draw
def checkDraw(text, scale_x, scale_y, r, position, x, y):
    # About line
    if position == 'left':
        angle = 135
        x_stop = x - scale_x
    
    elif position == 'right':
        angle = 45
        x_stop = x + scale_x
    
    y_stop = y + scale_y
    # Set line start position
    x_start = x + int((r-r//4) * math.cos(math.radians(angle)))
    y_start = y + int((r-r//4) * math.sin(math.radians(angle)))
    # Line
    line = Line(x_start, x_stop, y_start, y_stop, r//2)
    line.createLine()
    # Circle
    circle = Circle(x_stop, y_stop, r, text)
    circle.createCircle()
    circle.createText()
    
    return x_stop, y_stop

# Draw a Tree
def drawTree(root, r, scale_x, scale_y, x=0, y=0, position = 'root'):
    
    if type(root) == str:
        text = root.value
        checkDraw(text, scale_x//2, scale_y, r, position, x, y)
   
    elif root:
        
        text = root.value
        # Root position
        if position == 'root':
            
            x = scale_x // 2
            y = scale_y // 2
            
            circle = Circle(x, y, r, text)
            circle.createCircle()
            circle.createText()
            # Recursive
            drawTree(root.left, r, scale_x//2, scale_y, x, y, 'left')
            drawTree(root.right, r, scale_x//2, scale_y, x, y, 'right')
        
        else:
            # New position
            x, y = checkDraw(text, scale_x//2, scale_y, r, position, x, y)
            # Recursive
            drawTree(root.left, r, scale_x//2, scale_y, x, y, 'left')
            drawTree(root.right, r, scale_x//2, scale_y, x, y, 'right')

# Set Legend            
def drawLabel(infix):
    font = pygame.font.Font('freesansbold.ttf', 30)
    # Create text
    text_box = font.render(infix, True, (255,105,180), (255,192,203))
    text_rect = text_box.get_rect()
    # Pin text on screen
    screen.blit(text_box, text_rect)

# Use for compare
number = '0123456789'
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
operator = '!&+()'
operator_value = {'!':4, '&':3, '+':2, '(':1}

# Read file
f = open(r'D:\expression_tree\test.txt','r')
input_str = ''
for line in f.readlines():
    input_str += line

# Main
postfix = infix_to_postfix(input_str)
truthTable(postfix)
tree = create_expression_tree(postfix)
range_wide, range_height, radius = screenScale(tree, scr_w, scr_h)

# Start looping window
is_running = True
while is_running:

    for e in pygame.event.get():
        # Quit pygame
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
        # Screenshot
        elif e.type == KEYDOWN and e.key == K_SPACE:
            pygame.image.save(screen, 'example05.jpg')
    
    screen.fill((204, 255, 255))
    drawTree(tree, radius, scr_w, range_height)
    drawLabel(input_str)
        
    pygame.display.flip()

pygame.quit()
