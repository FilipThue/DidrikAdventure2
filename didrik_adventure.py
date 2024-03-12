# Tutorial for å forstå tiles: https://www.youtube.com/watch?v=Ongc4EVqRjo

import pygame
from settings import *
from sprites import *
from pygame.locals import *

pygame.init()

pygame.display.set_caption("Didrik Adventure 2")

# load images
bg_img = pygame.image.load('assets/img/background.png')


class World:
    def __init__(self, data):
        self.tile_list = []

        wall_img = pygame.image.load('assets/img/gulv.png')
        ground_img = pygame.image.load('assets/img/gulv_skole.png')
        spike_img = pygame.image.load('assets/img/spikes.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    self.tile_list.append((img, img_rect))
                if tile == 2:
                    img = pygame.transform.scale(ground_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    self.tile_list.append((img, img_rect))
                if tile == 3:
                    img = pygame.transform.scale(spike_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    self.tile_list.append((img, img_rect))

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            SCREEN.blit(tile[0], tile[1])
            pygame.draw.rect(SCREEN, (255, 255, 255), tile[1], 1)


class Game:
    def __init__(self, start_scene):
        self.scene = start_scene

    def run(self):
        run = True
        clock = pg.time.Clock()
        while run:
            clock.tick(FPS)
            SCREEN.blit(bg_img, (0, 0))

            next_scene = self.scene.update()
            if next_scene:
                self.scene = next_scene
            self.scene.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()


class Scene:
    def update(self):
        return self

    def draw(self):
        pass


class Level_scene(Scene):
    def __init__(self, world_d, player_pos):
        self.world = World(world_d)
        self.player = Player(player_pos[0], player_pos[1])

    def draw(self):
        self.world.draw()


class Level2(Level_scene):
    def __init__(self):
        super().__init__(world_data_2, (100, 0))

    def update(self):
        self.player.update(self.world)

        if self.player.rect.y > HEIGHT:
            pass
            # return Level2()


class Level1(Level_scene):
    def __init__(self):
        super().__init__(world_data_1, (100, HEIGHT - TILE_SIZE - 56))

    def update(self):
        self.player.update(self.world)

        if self.player.rect.y > HEIGHT:
            return Level2()


game = Game(Level1())
game.run()

pygame.quit()
