import pygame


def main():
    pygame.init()
    display = pygame.display.set_mode((1000, 800))
    cl = pygame.time.Clock()
    r = pygame.Rect(0, 0, 0, 0)

    drag = False
    mouse_down = False
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                print("Rectangle:"+str(p))

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                x = event.pos[0]
                y = event.pos[1]
                r.topleft = (x,y)
                r.width = 0
                r.height = 0
            

            if event.type == pygame.MOUSEMOTION:
                if mouse_down == True:
                    drag = True
                    x = event.pos[0]
                    y = event.pos[1]
                    r.width = x - r.x
                    r.height = y - r.y

        p = [r.top, r.left, r.right, r.bottom]
        display.fill((0,0,0))

        pygame.draw.rect(pygame.display.get_surface(), (255,0,0), r, 4) 
        pygame.display.flip()
        cl.tick(60)



if __name__ == '__main__': main()
