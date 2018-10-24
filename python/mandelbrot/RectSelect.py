import pygame


def main():
    pygame.init()
    display = pygame.display.set_mode((1000, 800))
    cl = pygame.time.Clock()
    r = pygame.Rect(100, 100, 100, 100)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                r.topleft = (x,y)

            if event.type == pygame.MOUSEMOTION:
                x = event.pos[0]
                y = event.pos[1]
                r.width = x - r.x
                r.height = y - r.y

        p = [r.top, r.left, r.right, r.bottom]
        print("Rect:"+str(r))
        print("XXX:"+str(p))
       # pygame.draw.lines(pygame.display.get_surface(), (255,0,0), True,[[10,10], [100,100]]) 
        display.fill((0,0,0))

        pygame.draw.rect(pygame.display.get_surface(), (255,0,0), r, 4) 
        pygame.display.flip()
        cl.tick(60)



if __name__ == '__main__': main()
