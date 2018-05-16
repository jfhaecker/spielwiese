import sys
import timeit
import time
import numpy
import pygame
from pygame.locals import * 
#from pygame import Color
from colour import Color

schwefelgelb = Color("#f1dd38")
verkehrsrot = Color("#bb1e10")
leuchtorange = Color("#ff4d06")
maxcolors = 700
#farbliste = [schwefelgelb, verkehrsrot, leuchtorange] #.range_to(verkehrsrot, 1000))
farbliste = list(schwefelgelb.range_to(verkehrsrot, maxcolors))
#print("Liste:",farbliste)

GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE =  (0, 0, 255)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

PIXELINFO = [ [0 for x in range(SCREEN_HEIGHT) ] for y in range(SCREEN_WIDTH)]
#print PIXELINFO

COMPLEX_PLANE_RE_MIN = -0.74877#-2
COMPLEX_PLANE_IMG_MIN =  0.06505#-1.25



COMPLEX_PLANE_RE_MAX = -0.74872#1
COMPLEX_PLANE_IMG_MAX = 0.06510#1.25

MAX_ITERATIONS = 1000

countstats = numpy.zeros( (MAX_ITERATIONS +1), dtype=numpy.int16 )
#print countstats

def mandel(z, maxiter):
    c = z
    for n in range(1, maxiter):
        if abs(z) > 2:
            return n
        z = z*z + c
        #print(z,": ",abs(z))
    return maxiter
     
    
def mapColor(count):
    countstats[count]+=1
    if count == MAX_ITERATIONS: 
        return Color('black')

    ret = farbliste[count % maxcolors]
    #rgbvar2 = [x * 255.0 for x in ret]
    
    #print("Return color for", count, ":",ret)
    
    return ret
    if(count < 3):
        return (255,0,0)
    if(count < 10):
        return (230,00,0)
    if(count < 30):
        return (200,00,0)
    if(count  < 50):
        return (150,0,0)
    
    return GREEN#(count % 255, 0, 0)

def mymandel():
    (x_samples, x_spacing) = numpy.linspace(COMPLEX_PLANE_RE_MIN, COMPLEX_PLANE_RE_MAX, num=SCREEN_WIDTH, retstep=True)
    print "X_spaceing {a:>30}".format(a=x_spacing)
    (y_samples, y_spacing) = numpy.linspace(COMPLEX_PLANE_IMG_MIN, COMPLEX_PLANE_IMG_MAX, num=SCREEN_HEIGHT, retstep=True)
    print "X_spaceing {a:>30}".format(a=y_spacing)
    #A two dimensional array, like its surface, is indexed [column, row]
    for row in range(SCREEN_HEIGHT ):
        for col in range(SCREEN_WIDTH ):
            c = complex(x_samples[col], y_samples[row])
            itercount = mandel(c, MAX_ITERATIONS)
            PIXELINFO[col][row] = [c, itercount]
            d = mapColor(itercount)
            pygame.display.get_surface().set_at( (col, row), pygame.Color(d.hex_l))
         
    printStats(countstats)


def printStats(stats):
    print("Stats for mandelbrot with Maxiter=", MAX_ITERATIONS, "(Iterations->Quantity)")
    k = 0
    for i,f in enumerate(stats):
        k += f
        print(i,"->",f)
    print("Total Numer of Complex Points checked: %s" %k)

def mandelbrot():
    mymandel()


if __name__ == '__main__':
    pygame.init()
    DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hello")
    DISPLAY.fill(GREEN)
    PIXELS = pygame.PixelArray(DISPLAY)
    
    s="from __main__ import mandelbrot"
    res = timeit.timeit("mandelbrot()", setup=s, number=1)
    print("Mandel tooks %ss" % res)
    

    cl = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                del PIXELS
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                x = event.pos[0]
                y = event.pos[1]
                print("Mouse at View(x,y): {a:>3},{b:>3} Complex(re,im): {d:>38}, Color: {c:>6}  Iterations: {e:>3}".format(a=x, b=y, c=pygame.display.get_surface().get_at((x, y)), d=PIXELINFO[x][y][0], e=PIXELINFO[x][y][1]))

                pygame.display.update()
        cl.tick(30)