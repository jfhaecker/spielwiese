import sys
import time
import numpy
import pygame
import Mandelfarben
from tqdm import tqdm

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

PIXELINFO = [ [0 for x in range(SCREEN_HEIGHT) ] for y in range(SCREEN_WIDTH)]
#print PIXELINFO

COMPLEX_PLANE_RE_MIN = -2#-0.74877#-2
COMPLEX_PLANE_IMG_MIN = -1.25#  0.06505#-1.25



COMPLEX_PLANE_RE_MAX = 1#-0.74872#1
COMPLEX_PLANE_IMG_MAX = 1.25#0.06510#1.25

MAX_ITERATIONS = 10

#countstats = numpy.zeros( (MAX_ITERATIONS +1), dtype=numpy.int16 )
#print countstats

def mandel(z, maxiter):
    c = z
    for n in range(1, maxiter):
        if abs(z) > 2:
            return n
        z = z*z + c
        #print(z,": ",abs(z))
    return maxiter
     
    
def mymandel():
    (x_samples, x_spacing) = numpy.linspace(COMPLEX_PLANE_RE_MIN, COMPLEX_PLANE_RE_MAX, num=SCREEN_WIDTH, retstep=True)
    print("X_spaceing {a:>30}".format(a=x_spacing))
    (y_samples, y_spacing) = numpy.linspace(COMPLEX_PLANE_IMG_MIN, COMPLEX_PLANE_IMG_MAX, num=SCREEN_HEIGHT, retstep=True)
    print("X_spaceing {a:>30}".format(a=y_spacing))
    
    #A two dimensional array, like its surface, is indexed [column, row]
    for row in tqdm(range(SCREEN_HEIGHT ), desc="Zeilen"):
        for col in range(SCREEN_WIDTH ):
            c = complex(x_samples[col], y_samples[row])
            itercount = mandel(c, MAX_ITERATIONS)
            d = Mandelfarben.mapColor(itercount, MAX_ITERATIONS)
            PIXELINFO[col][row] = [c, itercount, d]
            pygame.display.get_surface().set_at( (col, row), d)
    #printStats(countstats)


def printStats(stats):
    print("Stats for mandelbrot with Maxiter=", MAX_ITERATIONS, "(Iterations->Quantity)")
    k = 0
    for i,f in enumerate(stats):
        k += f
        print(i,"->",f)
    print("Total Numer of Complex Points checked: %s" %k)

def mandelbrot():
    mymandel()


def printPos(pos):
    x = pos[0]
    y = pos[1]
    print("_______________________________________________________")
    print("Screen(x,y): [{a:<3}][{b:<3}]".format(a=x, b=y))
    print("Complex:     [{a:<38}]".format(a=PIXELINFO[x][y][0]))
    print("Iterations:  [{a:<5}]".format(a=PIXELINFO[x][y][1]))
    print("Color:       [{a:<38}]".format(a=PIXELINFO[x][y][2]))



def printRect(rect):
    print("Rect(p1, p2, p3, p4): [{a:<3},{b:<3},{c:<3},{d:<3}]".format(a=rect[0], b=rect[1], c=rect[3], d=rect[4]))
    

def ende():
    print("Ende")
    #del PIXELS
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hello")
   # DISPLAY.fill(GREEN)
    PIXELS = pygame.PixelArray(DISPLAY)
    
    mandelbrot()


    cl = pygame.time.Clock()
    mousedown = False
    selectRectX = 0
    selectTextY = 0
    selection_rect = [ (0,0), (0,0), (0,0), (0,0) ] 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ende()
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   ende()
            if event.type == pygame.MOUSEMOTION:
                x = event.pos[0]
                y = event.pos[1]
                if(mousedown == False):
                    printPos(event.pos)
                else:
                    printRect(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
                print("MouseDown:"+str(mousedown))
                x = event.pos[0]
                y = event.pos[1]
                selectRectX = x
                selectRectY = y
            if event.type == pygame.MOUSEBUTTONUP:
                mousedown = False
                print("MauseDown:"+str(mousedown))
            
            display = pygame.display
            pygame.draw.lines(display.get_surface(), Mandelfarben.RED, True, selection_rect, 100)
            #display.update()
            display.flip()
        cl.tick(30)
