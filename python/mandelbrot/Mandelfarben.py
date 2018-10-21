from colour import Color as ColourColor
from pygame import Color as PyGameColor

GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE =  (0, 0, 255)
WHITE = (255, 255, 255)



schwefelgelb = ColourColor("#f1dd38")
verkehrsrot = ColourColor("#bb1e10")
leuchtorange = ColourColor("#ff4d06")
maxcolors = 20
farbliste = list(schwefelgelb.range_to(verkehrsrot, maxcolors))
#print("Liste:",farbliste)


def mapColor(count, max_iter):
    if count == max_iter: 
        return PyGameColor(0x000000)
    

    c = farbliste[count % maxcolors]
    return PyGameColor(c.hex_l)

