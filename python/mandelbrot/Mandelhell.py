import numpy as np 
from numba import jit
from matplotlib import pyplot as plt
from matplotlib import colors 

@jit
def mandelbrot(c, maxiter):
    z = c
    for n in range(maxiter):
        if(abs(z) > 2):
            return n
        z = z*z + c
    return 0

@jit
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, maxiter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in range(width):
        for j in range(height):
            n3[i,j] = mandelbrot(r1[i] + 1j*r2[j], maxiter)
    return(r1, r2, n3)


def mandelbrot_image(xmin, xmax, ymin, ymax, width, height, maxiter, cmap='jet'):
    dpi = 100
    img_width = width * dpi
    img_height = height * dpi
    ticks = np.arange(0, img_width, 1*dpi)
    print("Ticks {a}".format(a=ticks))
    print("....> {a}".format(a=ticks/img_width))
    print("Length:{a}".format(a=xmax-xmin))
    x_ticks = xmin + (xmax-xmin)*ticks/img_width
    print("XTicks {a}".format(a=x_ticks))
    x,y,z = mandelbrot_set(xmin, xmax, ymin, ymax, img_width, img_height, maxiter)
    print("Hallo")
    print(z.T)
    plt.figure(figsize=(width,height), dpi=dpi)
   # plt.xticks([100, 300,400, 500, 600], ['A', 'B', 'C'])
    
    ticks = np.linspace(0, img_width, 4)
    x_ticks = np.linspace(xmin, xmax, 4)
    
    x_ticks = x_ticks.round(decimals=2)
    print("TicksNeu {a}".format(a=ticks))
    print("XTicksNeu {a}".format(a=x_ticks))
    
    plt.xticks(ticks, x_ticks)

    norm = colors.PowerNorm(0.3)
    plt.imshow(z.T,cmap=cmap, origin='lower', norm=norm)
   # plt.hist(z.T, histtype="stepfilled", bins=100, facecolor="green")
    plt.show()

mandelbrot_image(-2.0, 0.5, -1.25, 1.25, 9,9, 1000, cmap='gnuplot2')


