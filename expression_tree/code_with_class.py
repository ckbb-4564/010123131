import pygame
import math
import sys
from pygame.locals import *

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

pygame.init()

scr_w, scr_h = 500, 500

screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption('Assignment 1') 

surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

def infix_to_postfix(infix):
    global number, alphabet, operator, operator_value
    operator_stack = Stack()
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
                while token != '(':
                    postfix.append(token)
                    token = operator_stack.pop()
            elif item in operator:
                if operator_stack.is_empty():
                    operator_stack.push(item)
                else:
                    token = operator_stack.top()
                    
                    if operator_value[item] > operator_value[token]:
                        operator_stack.push(item)
                    else:
                        state = True
                        while (not operator_stack.is_empty()) and operator_value[item] < operator_value[token] and state:
                            temp = operator_stack.pop()
                            if not operator_stack.is_empty():
                                token = operator_stack.top()
                            else:
                                state = False
                            postfix.append(temp)
                        operator_stack.push(item)
    while not operator_stack.is_empty():
        token = operator_stack.pop()
        postfix.append(token)
    return postfix

def create_expression_tree(expression):
    global number, alphabet, operator
    tree_stack = Stack()
    for item in postfix:
        if item == '!':
            child = tree_stack.pop()
            expression_tree = Expression_Tree(item)
            expression_tree.left = child
            tree_stack.push(expression_tree)
        elif item in operator:
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

def preOrder(root):
    return ([root.value] + preOrder(root.left) + preOrder(root.right)) if root else []

def findDepth(root):
    if root:
        left = findDepth(root.left)
        right = findDepth(root.right)
        return max(left, right) + 1
    else:
        return 0

def screenScale(root, scr_w, scr_h):
    global operator
    depth = findDepth(root)
    leaf = 2 ** depth
    rw = scr_w // leaf
    rh = scr_h // depth
    r = rw
    scale_y_line = ((rh // 2) - r) * 2
    scale_x_line = scr_w // 4
    return rw, rh, r, scale_x_line, scale_y_line

def checkDraw(text, scale_x, scale_y, r, position, x, y):
    if position == 'left':
        angle = 135
        x_stop = x - scale_x
    elif position == 'right':
        angle = 45
        x_stop = x + scale_x
    y_stop = y + scale_y

    x_start = x + int((r-r//4) * math.cos(math.radians(angle)))
    y_start = y + int((r-r//4) * math.sin(math.radians(angle)))
    line = Line(x_start, x_stop, y_start, y_stop, r//2)
    line.createLine()

    circle = Circle(x_stop, y_stop, r, text)
    circle.createCircle()
    circle.createText()
    return x_stop, y_stop

def drawTree(root, r, scale_x, scale_y, x=0, y=0, position = 'root'):
    if type(root) == str:
        text = root.value
        checkDraw(text, scale_x//2, scale_y, r, position, x, y)
    elif root:
        text = root.value
        if position == 'root':
            temp = scale_x//2
            x = scale_x // 2
            y = scale_y // 2
            circle = Circle(x, y, r, text)
            circle.createCircle()
            circle.createText()
            drawTree(root.left, r, scale_x//2, scale_y, x, y, 'left')
            drawTree(root.right, r, scale_x//2, scale_y, x, y, 'right')
        else:
            x, y = checkDraw(text, scale_x//2, scale_y, r, position, x, y)
            drawTree(root.left, r, scale_x//2, scale_y, x, y, 'left')
            drawTree(root.right, r, scale_x//2, scale_y, x, y, 'right')

def drawLabel(infix):
    font = pygame.font.Font('freesansbold.ttf', 30)
    text_box = font.render(infix, True, (255,105,180), (255,192,203))
    text_rect = text_box.get_rect()
    screen.blit(text_box, text_rect)

def solve(postfix):
    solve_stack = Stack()
    for item in postfix:
        if item == '!':
            token = solve_stack.pop()
            token = not token
            solve_stack.push(token)
        elif item == '&':
            token_1 = solve_stack.pop()
            token_2 = solve_stack.pop()
            token = token_1 and token_2
            solve_stack.push(token)
        elif item == '+':
            token_1 = solve_stack.pop()
            token_2 = solve_stack.pop()
            token = token_1 or token_2
            solve_stack.push(token)
        elif item == '1':
            token = True
            solve_stack.push(token)
        elif item == '0':
            token = False
            solve_stack.push(token)
    return solve_stack.pop()

def countVariable(postfix):
    global operator
    variable_list = []
    size = 0
    for item in postfix:
        if item not in operator:
            if item not in variable_list:
                variable_list.append(item)
                size += 1
    return variable_list, size

def truthTable(postfix):
    variable_list, size = countVariable(postfix)
    temp_list = [] * size
    decimal = 2 ** size - 1
    allprob = bin(decimal).replace('0b', '')
    for i in range(0,allprob+1):
        binary = bin(i).replace('0b', '')
        if len(binary) == len(allprob):
            for i in range(len(binary)):
                temp_list[i] = binary[i]
            solve(postfix)

number = '0123456789'
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
operator = '!&+()'
operator_value = {'!':4, '&':3, '+':2, '(':1}

f = open(r'D:\expression_tree\test.txt','r')
input_str = ''
for line in f.readlines():
    input_str += line

postfix = infix_to_postfix(input_str)
truthTable(postfix)
tree = create_expression_tree(postfix)
range_wide, range_height, radius, scale_x_line, scale_y_line = screenScale(tree, scr_w, scr_h)

is_running = True
while is_running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            pygame.image.save(screen, 'example05.jpg')
    screen.fill((204, 255, 255))
    drawTree(tree, radius, scr_w, range_height)
    drawLabel(input_str)
        
    pygame.display.flip()

pygame.quit()