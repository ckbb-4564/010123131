import pygame
import pygame.camera
from pygame.locals import *
import sys

def open_camera( frame_size=(1280,720),mode='RGB'):
    pygame.camera.init()
    list_cameras = pygame.camera.list_cameras()
    print( 'Number of cameras found: ', len(list_cameras) )
    if list_cameras:
        camera = pygame.camera.Camera(list_cameras[0], frame_size, mode )
        return camera 
    return None 

def swap_image(first_pos,second_pos):
    global image_rect_all,scr_w,scr_h,M,N
    #find rect origin
    first_pos_column = first_pos[0]//(scr_w//M)
    first_pos_row = first_pos[1]//(scr_h//N)
    second_pos_column = second_pos[0]//(scr_w//M) 
    second_pos_row = second_pos[1]//(scr_h//N)
    #create temp rect and make old into None
    temp_first_rect = image_rect_all[first_pos_column][first_pos_row]
    image_rect_all[first_pos_column][first_pos_row] = None
    temp_second_rect = image_rect_all[second_pos_column][second_pos_row]
    image_rect_all[second_pos_column][second_pos_row] = None
    #put temp rect into None index
    image_rect_all[first_pos_column][first_pos_row] = temp_second_rect
    image_rect_all[second_pos_column][second_pos_row] = temp_first_rect

scr_w, scr_h = 1280,720
screen = pygame.display.set_mode((scr_w, scr_h))
pygame.init()
pygame.display.set_caption("Pygame Camera")
camera = open_camera()
if camera:
    camera.start()
else:
    print('Cannot open camera')
    sys.exit(-1)

M,N = 10,10
rw, rh = scr_w//M, scr_h//N
image_rect_all = []
#create M*N rects
for i in range(M):
    image_rect_set = []
    for j in range(N):
        rect = (i*rw, j*rh, rw, rh)
        image_rect_set.append(rect)
    image_rect_all.append(image_rect_set)

img = None
is_running = True
while is_running:
    img = camera.get_image()
    if img is None:
        continue
    #put image into created rects
    for i in range(M):
        for j in range(N):
            pygame.draw.rect( img, (0,255,0), image_rect_all[i][j], 1)
    
            screen.blit( img, (i*rw,j*rh),image_rect_all[i][j] )
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
            if img:
                pygame.image.save( img, 'image.jpg' )
        elif e.type == pygame.MOUSEBUTTONDOWN:
            mouse_click_pos = pygame.mouse.get_pos()
        elif e.type == pygame.MOUSEBUTTONUP:
            mouse_release_pos = pygame.mouse.get_pos()
            swap_image(mouse_click_pos,mouse_release_pos)

    pygame.display.flip()

camera.stop()