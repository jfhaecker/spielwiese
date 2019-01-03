import sys
import time
import pygame
import argparse as ap
import numpy as np
import pygame
import seaborn as sns
import colorsys as csys
from tqdm import tqdm
from numba import jit


def init_color(max_colors):
    colors = sns.color_palette("hls", 1000)
    return colors

@jit
def mapColor(count, max_iter, farben):
    #print("Map Color {a}".format(a=count))
    if count == 0:
        return (255, 0, 0, 0)

    c = farben[count % len(farben)]
    csys.hls_to_rgb(c[0], c[1], c[2])
    #return (c.red * 255, c.green * 255, c.blue * 255, 0) #PyGameColor(c.hex_l)
    return c

def get_args():
    parser = ap.ArgumentParser(description = "Haex da best")
    parser.add_argument("--width", help="Width of window",
                        default=800, type=int)
    parser.add_argument("--height", help="Height of window",
                        default= 800, type=int)
    parser.add_argument("--max_iter", help="Max iterations",
                        default=100, type=int)
    parser.add_argument("--xmin", help="XMin",
                        default=-2.0, type=float)
    parser.add_argument("--xmax", help="XMax",
                        default=1.25, type=float)
    parser.add_argument("--ymin", help="YMin",
                        default=-2.0, type=float)
    parser.add_argument("--ymax", help="YMax",
                        default=2.0, type=float)
    return parser.parse_args()


def printStats(stats):
    print("Stats for mandelbrot with Maxiter=", MAX_ITERATIONS, "(Iterations->Quantity)")
    k = 0
    for i,f in enumerate(stats):
        k += f
        print(i,"->",f)
    print("Total Numer of Complex Points checked: %s" %k)



def printPos(pos, PIXELINFO):
    #print(PIXELINFO)
    pass
    #x = pos[0]
    #y = pos[1]
    #print("_______________________________________________________")
    #print("Screen(x,y): [{a:<3}][{b:<3}]".format(a=x, b=y))
    #print("Complex:     [{a:<38}]".format(a=PIXELINFO[x][y][0]))
    #print("Iterations:  [{a:<5}]".format(a=PIXELINFO[x][y][1]))
    #print("Color:       [{a}]".format(a=str(PIXELINFO[x][y][2])))



def printRect(rect):
    print("Rect(p1, p2, p3, p4): [{a:<3},{b:<3},{c:<3},{d:<3}]"
            .format(a=rect[0], b=rect[1], c=rect[3], d=rect[4]))
#@jit
def mandelbrot(c, maxiter, horizon, log_horizon):
    z = c
    for n in range(maxiter):
        az = abs(z)
        if az > horizon:
            # WTF?
            return n - np.log(np.log(az))/np.log(2) + log_horizon 
        z = z*z + c
        #print(z,": ",abs(z))
    return 0 


#@jit
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter, pixel_info):

    farben = init_color(max_iter)
    print("RenderMandel: [{a},{b}][{c},{d}]".
            format(a=xmin, b=ymin, c=ymax, d=ymax)) 

    #geklaut
    horizon = 2.0 ** 40
    #keine Ahnung
    log_horizon = np.log(np.log(horizon))/np.log(2)


    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))

    #A two dimensional array, like its surface, is indexed [column, row]
    for row in tqdm(range(width ), desc="Zeilen"):
        for col in range(height ):
            c = complex(r1[row], r2[col])
            i = mandelbrot(c, max_iter, horizon, log_horizon)
            # index i aus der magischen log funktion wieder zu int machen
            # aber nicht einach abschneiden, sonst gibts farbbänder
            index = int(i*100)
            #print("Alter Index{a} neuer Index{b}".format(a=i, b=index))
            d = mapColor(index, max_iter, farben)

            #print("Color for index{a}:{b}".format(a=index, b=d))
            #n3[row, col] = d
            if(index > 0):
                c = pygame.Color(int(d[0] * 256), 
                                int(d[1] * 256) , 
                                int(d[2] * 256))
            else:
                c = pygame.Color(0, 0, 0)
            pygame.display.get_surface().set_at( (row, col), c)
    return (r1, r2)

def mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter, pixel_info):
    mandelbrot_set(xmin, xmax, ymin, ymax,
                            width, height,
                            max_iter, pixel_info)
    #pixel_info[col][row] = [c, itercount, d]
    #printStats(countstats)
    #return (histogramm, pixel_info)


def main():
    pygame.init()

    args = get_args()
    xmin, xmax, ymin, ymax = args.xmin, args.xmax, args.ymin,args.ymax, 
    width, height = args.width, args.height
    max_iter = args.max_iter

    print(max_iter)


    screen =  pygame.display.set_mode((width, height))
    pygame.PixelArray(screen)

    pixel_info = [ [0 for x in range(height) ] for y in range(width)]
    mandelbrot_image(
            xmin, xmax, ymin,ymax,
            width, height,
            max_iter, pixel_info)

    #print(str(histogramm))

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
