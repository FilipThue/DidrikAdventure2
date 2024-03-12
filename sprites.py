import pygame as py
from settings import *



class Player:
    def __init__(self, x, y):
        img = py.image.load('assets/sprites/Didrik/didrikchilling.png')
        self.img = py.transform.scale(img, (5 * 7, 8 * 7))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.vel_y = 0
        self.jumped = False
        self.down = False

    def update(self, world):
        key = py.key.get_pressed()
        delta = [0, 0]

        if (key[py.K_UP] or key[py.K_SPACE]) and self.jumped == False:
            self.vel_y = -30
            self.jumped = True
        if (key[py.K_UP] or key[py.K_SPACE]) == False:
            self.jumped = False


        if key[py.K_LEFT] or key[py.K_a]:
            delta[0] -= 5
        if key[py.K_RIGHT] or key[py.K_d]:
            delta[0] += 5

        self.vel_y += 2
        if self.vel_y > 20:
            self.vel_y = 20
        delta[1] += self.vel_y

        #kollisjoner
        for tile in world.tile_list:
            # x
            if tile[1].colliderect(self.rect.x  + delta[0], self.rect.y, self.width, self.height):  # tile[0] er bildet
                delta[0] = 0
                print(tile[1])

            # y
            if tile[1].colliderect(self.rect.x, self.rect.y + delta[1], self.width, self.height):
                if self.vel_y >= 0:  # sjekker om han står på bakken
                    delta[1] = tile[1].top - self.rect.bottom
                    #self.vel_y = 0
                elif self.vel_y < 0:  # sjekker om han dunker hodet
                    delta[1] = tile[1].bottom - self.rect.top
                    self.vel_y = 0

        self.rect.x += delta[0]
        self.rect.y += delta[1]


        self.draw()

    def draw(self):
        pg.draw.rect(SCREEN, (255, 0, 0), self.rect)
        SCREEN.blit(self.img, self.rect)

