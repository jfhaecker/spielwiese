
""" Jetzt wird noch mehr gemandelt """

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


class ScreenInfo:
    def __init__(self, screen_x, screen_y, pos_complex, iterations, n_iter, nm_iter, abs_complex, color):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.pos_complex = pos_complex
        self.iterations = iterations
        self.n_iter = n_iter
        self.nm_iter = nm_iter
        self.abs_complex = abs_complex
        self.color = color

    def __str__(self):
        x = ("Screen(x,y): [{a:<3}][{b:<3}]".format(a=self.screen_x,
                                                    b=self.screen_y))
        y = ("Complex:     [{a:<38}]".format(a=self.pos_complex))
        w = ("Abs(Z):      [{a:<38}]".format(a=self.abs_complex))
        u = ("Iterations:  [{a:<5}][{b:<5}][{c:<5}]".format(a=self.iterations,
                                                            b=self.n_iter,
                                                            c=self.nm_iter))
        v = ("Color:       [{a}]".format(a=self.color))
        return x + "\n" + y +"\n" + w +"\n" + u + "\n" + v

def init_color(max_colors):
    colors = sns.hls_palette(100,  l=.3, s=.8)
    return colors

@jit
def mapColor(count, max_iter, farben):

    c = farben[count % len(farben)]
    d = csys.hls_to_rgb(c[0], c[1], c[2])
    pixel_color = pygame.Color(0, 0, 0)
    if(count > 0):
         pixel_color = pygame.Color(int(d[0] * 256), 
                        int(d[1] * 256) , 
                        int(d[2] * 256))
    return pixel_color

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



def printPos(pos, screen_infos):
    #print(PIXELINFO)
    x = pos[0]
    y = pos[1]
    info = screen_infos[x][y]
    print("_______________________________________________________")
    print(info)


def printRect(rect):
    #print("Rect(p1, p2, p3, p4): [{a:<3},{b:<3},{c:<3},{d:<3}]".format(a=rect.topleft,
    print("Rect(p1, p2, p3, p4): [{a},{b},{c},{d}]".format(a=rect.topleft,
                                b=rect.bottomleft, c=rect.topright, d=rect.bottomright))
#@jit
def mandelbrot(c, maxiter, horizon, log_horizon):
    z = c
    for n in range(maxiter):
        az = abs(z)
        if az > horizon:
            return (n, az)
        z = z*z + c
    return (0,0) 

def get_complex_coords(xmin, xmax, ymin, ymax, width, height):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymax, ymin, height) #reverse
    return (r1, r2)

#@jit
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter, screen_infos):
    surface = pygame.Surface((width, height))
    farben = init_color(max_iter)
    print("RenderMandel: [{a},{b}][{c},{d}]".format(a=xmin, b=ymin, c=xmax, d=ymax)) 
    update_screen_every_row = 100
    #geklaut
    horizon = 2.0 ** 40 
    log_horizon = np.log(np.log(horizon))/np.log(2)
    (r1, r2) = get_complex_coords(xmin, xmax, ymin, ymax, width, height)

    for row in tqdm(range(width ), desc="Zeilen"):
        for col in range(height ):
            c = complex(r1[col], r2[row])
            (n, az) = mandelbrot(c, max_iter, horizon, log_horizon)
            nk = 0
            if(n > 0):
                #wtf
                nk = n - np.log(np.log(az))/np.log(2) + log_horizon 
                # index i aus der magischen log funktion wieder zu int machen
                # aber nicht einach abschneiden, sonst gibts farbbänder
                index = int(nk*10)
            else:
                index = 0
            color = mapColor(index, max_iter, farben)
            screen_infos[col][row] = ScreenInfo(col, row, c,
                                                n, nk,index, az, color)
            surface.set_at( (col, row), color)
           # if (row % update_screen_every_row == 0):
           #  display = pygame.display.flip()
    return surface

def mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter, pixel_info):
    return mandelbrot_set(xmin, xmax, ymin, ymax,
                            width, height,
                            max_iter, pixel_info)


def main():
    pygame.init()

    print(pygame.display.Info())
    args = get_args()
    xmin, xmax, ymin, ymax = args.xmin, args.xmax, args.ymin,args.ymax, 
    width, height = args.width, args.height
    max_iter = args.max_iter

    screen =  pygame.display.set_mode((width, height))
    mouse_down, running = False, True
    render_next = True
    selection_rect = pygame.Rect(0, 0, width, height)
    pixel_info = [ [0 for x in range(height) ] for y in range(width)]
    while(running):
        if (render_next):
            pixel_info = [ [0 for x in range(height) ] for y in range(width)]
            surface = mandelbrot_image( xmin, xmax, ymin,ymax, 
                                    width, 
                                    height,
                                    max_iter, pixel_info)
            #xmin = pixel_infos[][]
            #xmax = pixel_info
            render_next = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   running = False
            #MOUSEMOTION
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos[0], event.pos[1]
                if(mouse_down == False):
                    printPos(event.pos, pixel_info)
                else:
                    selection_rect.width = x - selection_rect.x
                    selection_rect.height = y - selection_rect.y
                    #printRect(selection_rect)
            #MOUSEDOWN
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y, mouse_down = event.pos[0], event.pos[1], True
                selection_rect.topleft = (x, y)
                selection_rect.width, selection_rect.height = 0, 0
                print("MouseDown:"+str(mouse_down))
            #MOUSEUP
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                render_next = True
                print("MouseDown! New Mandelbrot: {a}".format(a=selection_rect))
                x1 = pixel_info[selection_rect.topleft[0]][selection_rect.topleft[1]]
                x2 = pixel_info[selection_rect.bottomright[0]][selection_rect.bottomright[1]]
                x3 = pixel_info[selection_rect.bottomleft[0]][selection_rect.bottomleft[1]]
                x4 = pixel_info[selection_rect.topright[0]][selection_rect.topright[1]]
                print("topleft:{a}".format(a=x1))
                print("bottomright:{a}".format(a=x2))
                print("bottomleft:{a}".format(a=x3))
                print("topright:{a}".format(a=x4))
                print("XMin=>{a}".format(a=x3.pos_complex.real))
                print("YMin=>{a}".format(a=x3.pos_complex.imag))
                print("XMax=>{a}".format(a=x4.pos_complex.real))
                print("YMax=>{a}".format(a=x4.pos_complex.imag))
                xmin = x3.pos_complex.real
                ymin = x3.pos_complex.imag
                xmax = x4.pos_complex.real
                ymax = x4.pos_complex.imag

        screen = pygame.display.get_surface()
        screen.blit(surface,(0, 0))
        pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), selection_rect, 4)
        display = pygame.display.flip()
        pygame.time.Clock().tick(30)
    
    
    
    pygame.quit()


if __name__ == '__main__':main()
