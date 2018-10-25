import sys
import time
import numpy
import pygame
import Mandelfarben
import argparse as ap
from tqdm import tqdm


#PIXELINFO = None
#print PIXELINFO

COMPLEX_PLANE_RE_MIN = -2#-0.74877#-2
COMPLEX_PLANE_IMG_MIN = -1.25#  0.06505#-1.25



COMPLEX_PLANE_RE_MAX = 1#-0.74872#1
COMPLEX_PLANE_IMG_MAX = 1.25#0.06510#1.25


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


def mymandel(width, height, max_iter, pixel_info):
    (x_samples, x_spacing) = numpy.linspace(COMPLEX_PLANE_RE_MIN,
                                            COMPLEX_PLANE_RE_MAX,
                                            num=width,
                                            retstep=True)
    #print("X_spaceing {a:>30}".format(a=x_spacing))
    (y_samples, y_spacing) = numpy.linspace(COMPLEX_PLANE_IMG_MIN,
                                            COMPLEX_PLANE_IMG_MAX,
                                            num=height,
                                            retstep=True)
    #print("X_spaceing {a:>30}".format(a=y_spacing))

    #A two dimensional array, like its surface, is indexed [column, row]
    for row in tqdm(range(height ), desc="Zeilen"):
        for col in range(width ):
            c = complex(x_samples[col], y_samples[row])
            itercount = mandel(c, max_iter)
            d = Mandelfarben.mapColor(itercount, max_iter)
            pixel_info[col][row] = [c, itercount, d]
            pygame.display.get_surface().set_at( (col, row), d)
    #printStats(countstats)


def printStats(stats):
    print("Stats for mandelbrot with Maxiter=", MAX_ITERATIONS, "(Iterations->Quantity)")
    k = 0
    for i,f in enumerate(stats):
        k += f
        print(i,"->",f)
    print("Total Numer of Complex Points checked: %s" %k)



def printPos(pos, PIXELINFO):
    x = pos[0]
    y = pos[1]
    print("_______________________________________________________")
    print("Screen(x,y): [{a:<3}][{b:<3}]".format(a=x, b=y))
    print("Complex:     [{a:<38}]".format(a=PIXELINFO[x][y][0]))
    print("Iterations:  [{a:<5}]".format(a=PIXELINFO[x][y][1]))
    print("Color:       [{a:<38}]".format(a=PIXELINFO[x][y][2]))



def printRect(rect):
    print("Rect(p1, p2, p3, p4): [{a:<3},{b:<3},{c:<3},{d:<3}]"
            .format(a=rect[0], b=rect[1], c=rect[3], d=rect[4]))


def ende():
    print("Ende")
    #del PIXELS
    pygame.quit()
    sys.exit()


def get_args():
    parser = ap.ArgumentParser(description = "Haex da best")
    parser.add_argument("--window_width", help="Width of window",
                        default=800, type=int)
    parser.add_argument("--window_height", help="Height of window",
                        default= 600, type=int)
    parser.add_argument("--max_iter", help="Max iterations",
                        default=100, type=int)
    parser.add_argument("--complex_topleft", help="Topleft complex number",
                        default="-2+1.25j", type=complex)
    parser.add_argument("--complex_width", help="Mandel width",
                        default=2.0, type=float)
    parser.add_argument("--complex_height", help="Mandel height",
                        default=2.0, type=float)
    return parser.parse_args()


def main():
    pygame.init()
    pygame.display.set_caption("Hello")

    args = get_args()
    w_width = args.window_width
    w_height = args.window_height
    pixel_info = [ [0 for x in range(w_height) ] for y in range(w_width)]
    DISPLAY = pygame.display.set_mode((w_width, w_height))
    PIXELS = pygame.PixelArray(DISPLAY)
    mymandel(w_width, w_height,args.max_iter, pixel_info)
    
    
    
    
    cl = pygame.time.Clock()
    mousedown = False
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
                    printPos(event.pos, pixel_info)
                else:
                    printRect(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
                print("MouseDown:"+str(mousedown))
                x = event.pos[0]
                y = event.pos[1]
            if event.type == pygame.MOUSEBUTTONUP:
                mousedown = False
                print("MauseDown:"+str(mousedown))

        display = pygame.display
        pygame.draw.lines(display.get_surface(), Mandelfarben.RED, True, selection_rect, 100)
        #display.update()
        display.flip()
        cl.tick(30)


if __name__ == '__main__':main()
