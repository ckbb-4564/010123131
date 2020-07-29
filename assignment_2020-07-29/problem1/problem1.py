###################################################################
# File: pygame_camera_demo-1.py
# Date: 2020-07-25
###################################################################
import pygame
import pygame.camera
from pygame.locals import *
import sys

# For windows 10, install VideoCapture 
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#videocapture

# Open Terminal in VSCode and run the following command
# $  pip install VideoCapture 

def open_camera( frame_size=(1280,720),mode='RGB'):
    pygame.camera.init()
    list_cameras = pygame.camera.list_cameras()
    print( 'Number of cameras found: ', len(list_cameras) )
    if list_cameras:
        # use the first camera found
        camera = pygame.camera.Camera(list_cameras[0], frame_size, mode )
        return camera 
    return None 

def toggleimg():
    global M, N, rw, rh, black_lists, remove_lists
    mouse_pos = pygame.mouse.get_pos()
    for i in range(M):
        x_range = range(i*rw, i*rw + rw)
        for j in range(N):
            y_range = range(j*rh, j*rh + rh)
            if mouse_pos[0] in x_range and mouse_pos[1] in y_range:
                remove_rect = (i*rw, j*rh, rw, rh)
                if remove_rect in black_lists:
                    black_lists.remove(remove_rect)
                    remove_lists.append(remove_rect)

scr_w, scr_h = 1280,720
pygame.init()
pygame.display.set_caption("Pygame Camera")
camera = open_camera()
if camera:
    camera.start()
else:
    print('Cannot open camera')
    sys.exit(-1)

screen = pygame.display.set_mode((scr_w, scr_h))

surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

M,N = 10,10
rw, rh = scr_w//M, scr_h//N
black_lists = []
remove_lists = []
for i in range(M):
    for j in range(N):
        black_rect = (i*rw, j*rh, rw, rh)
        if black_rect not in black_lists:
            black_lists.append(black_rect)

img = None
is_running = True 
while is_running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
            if img:
                # save the current image into the output file
                pygame.image.save( img, 'image.jpg' )
        if e.type == pygame.MOUSEBUTTONDOWN:
            toggleimg()
    
    # try to capture the next image from the camera 
    img = camera.get_image()
    if img is None:
        continue

    # get the image size
    img_rect = img.get_rect()
    img_w, img_h = img_rect.w, img_rect.h
    
    if len(black_lists) > 0:
        for black in black_lists:
            pygame.draw.rect( surface, (0,255,0), black, 1)
    
    if len(remove_lists) > 0:
        for rmv in remove_lists:
            surface.blit(img,rmv,rmv)

    # write the surface to the screen and update the display
    screen.blit( surface, (0,0) )
    pygame.display.flip()

# close the camera
camera.stop()

print('Done....')
###################################################################