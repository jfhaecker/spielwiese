
""" Jetzt wird noch mehr gemandelt """

import sys
import time
import pygame
import argparse as ap
import numpy as np
import pygame
from tqdm import tqdm
from numba import jit
from math import log,log2,floor,ceil
from collections import defaultdict
from pygame.locals import *


count = 0

class ScreenInfo:
    def __init__(self, screen_x, screen_y, pos_complex, iterations, n_iter, nm_iter, abs_complex, color, hues, lerp_hue):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.pos_complex = pos_complex
        self.iterations = iterations
        self.n_iter = n_iter
        self.nm_iter = nm_iter
        self.abs_complex = abs_complex
        self.color = color
        self.hues = hues
        self.lerp_hue = lerp_hue

    def __str__(self):
        return f"Screen(x,y): [{self.screen_x}][{self.screen_y}]\n"  \
            f"Complex:     [{self.pos_complex:<38}]\n"            \
            f"Abs(Z):      [{self.abs_complex:<38}]\n"       \
            f"Iterations:  [{self.iterations:<5}][{self.n_iter:<5}][{self.nm_iter:<5}]\n"  \
            f"Color:       [{self.color},{self.color.hsva}]\n"  \
            f"Hue:         [{self.hues[floor(self.n_iter)]},{self.hues[ceil(self.n_iter)]}={self.lerp_hue}]\n"


def init_color(max_colors):
    #colors = sns.hls_palette(100,  l=.3, s=.8)
    colors = sns.hls_palette(100)
    return colors


def linear_interpolation(color1, color2, t):
    c =  color1 * (1 - t) + color2 * t 
    return c

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


def mapColor2(m, max_iter):
    r = int(255 * m / max_iter)
    g = int(255 * m / max_iter)
    b = int(255 * m / max_iter)
    return pygame.Color(r, g, b)

def mapColor3(m, max_iter):
    hue = int(360 * m / max_iter)
    saturation = 50
    value = 100 if m < max_iter else 0
    c = pygame.Color(0, 0,0)
    c.hsva = (hue, saturation, value, 0)
    return c

def mapColor4(hue, max_iter ,m):
    #print("MappingColor for {a} and max_iter {b} with hues {c}".format(a=m, b=max_iter, c=hues))
    saturation = 50.0
    value = 100 if m < max_iter else 0
    c = pygame.Color(0)
    c.hsva = (hue, saturation, value, 0)
    return c

def mapColor5(m, hues, max_iter):
    hue = 0
    if m < max_iter:
        hue = 360 - int(360 * hues[floor(m)])
    saturation = 50
    value = 100 if m < max_iter else 0
    c = pygame.Color()
    c.hsva = (hue, saturation, value, 0)
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
    parser.add_argument("--escape_radius", help="Mandelbrot escape radius",
                        default=2, type=int)
    return parser.parse_args()


def printStats(stats):
    print(f"Stats for mandelbrot with Maxiter={MAX_ITERATIONS} (Iterations->Quantity)")
    k = 0
    for i,f in enumerate(stats):
        k += f
        print(f"{i}->{f}")
    print(f"Total Numer of Complex Points checked: {k}")



def printPos(pos, screen_infos):
    x = pos[0]
    y = pos[1]
    info = screen_infos[x][y]
    print("_______________________________________________________")
    print(info)


def printRect(rect):
    print("Rect(p1, p2, p3, p4): [{a},{b},{c},{d}]".format(a=rect.topleft,
                                b=rect.bottomleft, c=rect.topright, d=rect.bottomright))
#@jit
# see https://linas.org/art-gallery/escape/smooth.html
def mandelbrot(c, max_iter, smooth, escape_radius):
    z = c
    for n in range(max_iter):
        if abs(z) > escape_radius:
            if smooth:
                log_magic = n + 1 - log (log (abs(z))) / log(2)
                ret = (n, log_magic, abs(z))
                return ret
            else:
                ret = (n, n, abs(z))
                return ret 
        z = z*z + c
    ret = (max_iter, max_iter, abs(z))
    return ret

def get_complex_coords(xmin, xmax, ymin, ymax, width, height):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymax, ymin, height) #reverse
    return (r1, r2)


def mandelbrot_histogramm(xmin, xmax, ymin, ymax, width, height, max_iter, screeninfos, escape_radius):
    histogram = defaultdict(lambda : 0)
    (r1, r2) = get_complex_coords(xmin, xmax, ymin, ymax, width, height)


    for row in tqdm(range(height), desc="Zeilen"):
        for col in range(width):
            c = complex(r1[col], r2[row])
            (n,_,_) = mandelbrot(c, max_iter, True, escape_radius)
            histogram[n] += 1

    print_histogram(histogram)

    hues = []
    hue = 0
    total = sum(histogram[i] for i in range(max_iter))
    for i in range(max_iter):
        hue += (histogram[i] / total)
        hues.append(hue)
    hues.append(hue)

    print_hues(hues)

    return hues


def print_hues(hues):
    print("Hues")
    for i in range(len(hues)):
        print(f"Hue[{i}]={hues[i]}")
    print(f"Sum of values {sum(hues)}")


def print_histogram(histogram):
    total = sum(histogram.values())
    print(f"Histogramm for {total} Pixel")
    for k, v in sorted(histogram.items()):
        print(f"Histogram[{k}]={v}")


#@jit
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter, screen_infos, escape_radius):

    hues = mandelbrot_histogramm(xmin, xmax, ymin, ymax, width, height, max_iter, screen_infos, escape_radius)
    
    surface = pygame.Surface((width, height))
    print(f"RenderMandel: [{xmin},{ymin}][{xmax},{ymax}][{width},{height}]") 
    (cx, cy) = get_complex_coords(xmin, xmax, ymin, ymax, width, height)

    for x in tqdm(range(width ), desc="Zeilen"):
        for y in range(height):
            c = complex(cx[x], cy[y])
            (n,m,z) = mandelbrot(c, max_iter, True, escape_radius)
            if m > max_iter:
                m = max_iter
            mm = m % 1
            hue = 360 - int(360 * linear_interpolation(hues[floor(m)], hues[ceil(m)], mm))
            color = mapColor4(hue, max_iter, m)
            screen_infos[x][y] = ScreenInfo(x, y, c, n, m, mm,z, color, hues, hue)
            surface.set_at( (x, y), color)
    return surface

def mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter, pixel_info, escape_radius):
    return mandelbrot_set(xmin, xmax, ymin, ymax,
                            width, height,
                            max_iter, pixel_info, escape_radius)


def main():
    pygame.init()

    print(pygame.display.Info())
    args = get_args()
    xmin, xmax, ymin, ymax = args.xmin, args.xmax, args.ymin,args.ymax, 
    width, height = args.width, args.height
    max_iter = args.max_iter
    screen =  pygame.display.set_mode((width, height) )
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
                                    max_iter, pixel_info, args.escape_radius)
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
