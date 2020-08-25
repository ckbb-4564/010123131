import pygame
from pygame.locals import *
from expression import Expression
from draw_tree import Draw_Tree
from read_file import read_file

pygame.init()

screen_width = 500

screen_height = 500


screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Assignment I')

font = pygame.font.Font('freesansbold.ttf', 30)

read_path = r'D:\expression_tree\Expression.txt' #Enter your full path of expression file
save_path = r'D:\expression_tree\picture' #Enter your full path of picture to save

data = read_file(read_path)
data_index = 0

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        elif event.type == KEYDOWN and event.key == K_SPACE:
            picture_number = data_index + 1
            pygame.image.save(screen, save_path+'\problem'+str(picture_number)+'.jpg')
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            data_index  = (data_index + 1) % len(data)
        elif event.type == KEYDOWN and event.key == K_LEFT:
            data_index  = (data_index - 1) % len(data)
    
    screen.fill((204, 255, 255))

    boolean_expression = Expression(data[data_index])
    boolean_expression.infix_to_postfix()
    boolean_expression.create_tree()

    tree_picture = Draw_Tree(boolean_expression.expression_tree)
    tree_picture.set_screen(screen_width, screen_height, screen)
    tree_picture.set_scale()
    tree_picture.draw(tree_picture.root, screen_width)

    text_box = font.render(data[data_index], True, (255,105,180), (255,192,203))
    text_rect = text_box.get_rect()
    screen.blit(text_box, text_rect)

    pygame.display.flip()

