from tqdm import tqdm
import sys
import time
import pygame
import argparse as ap
import Mandelbrot
import numpy
import pygame
from colour import Color as ColourColor
from pygame import Color as PyGameColor


def init_color(max_colors):
    schwefelgelb = ColourColor("#f1dd38")
    verkehrsrot = ColourColor("#bb1e10")
    leuchtorange = ColourColor("#ff4d06")
    farbliste = list(schwefelgelb.range_to(verkehrsrot, max_colors))
    #print("Liste:",farbliste)
    return farbliste

def mapColor(count, max_iter, farben):
    if count == max_iter:
        return (255, 255, 255, 0)

    c = farben[count % len(farben)]
    return (c.red, c.green, c.blue, 0) #PyGameColor(c.hex_l)


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
                        default=3.0, type=float)
    parser.add_argument("--complex_height", help="Mandel height",
                        default=2.5, type=float)
    parser.add_argument("--histogramm", help="View histogramm only")
    return parser.parse_args()


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

def mandel(z, maxiter):
    c = z
    for n in range(1, maxiter):
        if abs(z) > 2:
            return n
        z = z*z + c
        #print(z,": ",abs(z))
    return maxiter


def mymandel(width, height, c_topleft,c_width, c_height, max_iter):

    print("RenderMandel:  {a},{b},{c}".format(a=c_topleft, b=c_width, c=c_height)) 
    farben = init_color(max_iter)

    (x_samples, x_spacing) = numpy.linspace(c_topleft.real,
                                            c_topleft.real + c_width,
                                            num=width, retstep=True)
    #print("X_spaceing {a:>30}".format(a=x_spacing))
    (y_samples, y_spacing) = numpy.linspace(c_topleft.imag,
                                            c_topleft.imag - c_height,
                                            num=height, retstep=True)
    #print("X_spaceing {a:>30}".format(a=y_spacing))

    histogramm = numpy.zeros(max_iter + 1)
    pixel_info = [ [0 for x in range(height) ] for y in range(width)]

    #A two dimensional array, like its surface, is indexed [column, row]
    for row in tqdm(range(height ), desc="Zeilen"):
        for col in range(width ):
            c = complex(x_samples[col], y_samples[row])
            itercount = mandel(c, max_iter)
            histogramm[itercount] += 1 
            d = mapColor(itercount, max_iter, farben)
            pixel_info[col][row] = [c, itercount, d]
            pygame.display.get_surface().set_at( (col, row), d)
    #printStats(countstats)
    return histogramm, pixel_info


def main():
    pygame.init()

    args = get_args()
    w_width, w_height = args.window_width, args.window_height
    screen =  pygame.display.set_mode((w_width, w_height))
    pygame.PixelArray(screen)

    histogramm, pixel_info = Mandelbrot.mymandel(w_width, w_height,
            args.complex_topleft, args.complex_width, args.complex_height, 
            args.max_iter)

    print(str(histogramm))

    mouse_down, running = False, True
    selection_rect = [ (0,0), (0,0), (0,0), (0,0) ] 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   running = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos[0], event.pos[1]
                if(mouse_down == False):
                    printPos(event.pos, pixel_info)
                else:
                    printRect(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y, mouse_down = event.pos[0], event.pos[1], True
                print("MouseDown:"+str(mouse_down))
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                print("MauseDown:"+str(mouse_down))

        display = pygame.display.flip()
        pygame.time.Clock().tick(30)
    pygame.quit()

if __name__ == '__main__':main()
