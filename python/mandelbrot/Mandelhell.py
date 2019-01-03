import numpy as np 
from numba import jit
from matplotlib import pyplot as plt
from matplotlib import colors 

@jit
def mandelbrot(c, maxiter, horizon, log_horizon):
    z = c
    for n in range(maxiter):
        az = abs(z)
        if az > horizon:
            return n - np.log(np.log(az))/np.log(2) + log_horizon
        z = z*z + c
    return 0

@jit
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, maxiter):
    #magic math 
    horizon = 2.0 ** 40
    log_horizon = np.log(np.log(horizon))/np.log(2)
    #
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in range(width):
        for j in range(height):
            f = mandelbrot(r1[i] + 1j*r2[j], maxiter, horizon, log_horizon)
            n3[i,j] = f 
            if(f > 0 ):
                print("[{a}][{b}]={c}".format(a=i, b=j, c=f))
    return(r1, r2, n3)



def mandelbrot_image(xmin, xmax, ymin, ymax, width=6, height=6, maxiter=100, cmap='jet'):
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
    x_ticks = x_ticks.round(decimals=10)
    print("TicksNeu {a}".format(a=ticks))
    print("XTicksNeu {a}".format(a=x_ticks))
    plt.xticks(ticks, x_ticks)
    y_ticks = np.linspace(ymin, ymax, 4)
    y_ticks = y_ticks.round(decimals=10)
    plt.yticks(ticks, y_ticks)



    norm = colors.PowerNorm(0.3)
    print("z.T=>{a}".format(a=z.T))
    plt.imshow(z.T,cmap=cmap, origin='lower', norm=norm)
   # plt.hist(z.T, histtype="stepfilled", bins=100, facecolor="green")
    plt.show()

#mandelbrot_image(-2.0, 0.5, -1.25, 1.25, 9,9, 1000, cmap='hot')
#mandelbrot_image(-0.8,-0.7,0,0.1,maxiter=2000,cmap='hot')
mandelbrot_image(-0.75,-0.7473,0.063,0.06557,width=10, height=10,maxiter=20000,cmap='gnuplot2')




