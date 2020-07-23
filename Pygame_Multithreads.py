import threading
import time
import cmath
import pygame
from random import randint, randrange, random

print( 'File:', __file__ )

def mandelbrot(c,max_iters=100):
    i = 0
    z = complex(0,0)
    while abs(z) <= 2 and i < max_iters:
        z = z*z + c
        i += 1 
    return i

# initialize pygame
pygame.init()

# create a screen of width=600 and height=400
scr_w, scr_h = 500, 500
screen = pygame.display.set_mode( (scr_w, scr_h) )

# set window caption
pygame.display.set_caption('Fractal Image: Mandelbrot') 

# create a clock
clock = pygame.time.Clock()

# create a surface for drawing
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

running = True
w2, h2 = scr_w/2, scr_h/2 # half width, half screen

def thread_func(id, surface, lock, barrier):
    global create
    x_start = (id - 1) * 5 + 1
    x_stop = x_start + 100
    y_start = 1
    y_stop = 500 
    scale = 0.006
    offset = complex(-0.55, 0.0)
    #if sem.acquire(timeout=0.1):
    while x_start < x_stop:
        while y_start <= y_stop:
            re = scale * (x_start - w2) + offset.real
            im = scale * (y_start - h2) + offset.imag
            c = complex(re, im)
            color = mandelbrot(c, 63)
            r = (color << 6) & 0xc0
            g = (color << 4) & 0xc0
            b = (color << 2) & 0xc0
            #print('{} worked.'.format( threading.currentThread().getName() ) )
            with lock:
                surface.set_at((x_start, y_start), (255-r, 255-g, 255-b))
            try:
                barrier.wait()
            except threading.BrokenBarrierError:
                pass
            #print('{} y = {}.'.format( threading.currentThread().getName(), y_start) )
            y_start += 1
        #print('{} x = {}.'.format( threading.currentThread().getName(), x_start) )
        y_start = 1
        x_start += 1
    #print('{} finished.'.format( threading.currentThread().getName() ) )


# set the number of threads to be created
N = 100

# create a thread lock 
lock = threading.Lock()

# create a barrier
barrier = threading.Barrier(N+1)

# a list for keeping the thread objects
list_threads = []

for i in range(N):
    id = (i+1)
    t = threading.Thread(target=thread_func, args=(id,surface,lock,barrier))
    t.setName( 'Thread-{:03d}'.format(id) )
    list_threads.append( t )

# start threads
for t in list_threads:
    t.start()

while running:
    clock.tick(120)
    create = True
    #for sem in list_semaphores:
        #sem.release()
    try:
        barrier.wait()
    except threading.BrokenBarrierError:
        pass

    with lock:
        # draw the surface on the screen
        screen.blit( surface, (0,0) )
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()