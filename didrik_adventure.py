# Tutorial for å forstå tiles: https://www.youtube.com/watch?v=Ongc4EVqRjo

import pygame
from settings import *
from sprites import *
from pygame.locals import *

pygame.init()
font = pg.font.Font("assets/font/Grand9KPixel.ttf", 40)

pygame.display.set_caption("Didrik Adventure 2")

# load images
bg_img = pygame.image.load('assets/backdrops/level1.png')
bg_img_level2 = pygame.image.load('assets/backdrops/level2.png')
bg_img_level2_5 = pygame.image.load('assets/backdrops/level2_5.png')
bg_img_level3 = pygame.image.load('assets/backdrops/level3.png')
bg_img_level4 = pygame.image.load('assets/backdrops/level4.png')
bg_img_level5 = pygame.image.load('assets/backdrops/level5.png')


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
                    self.tile_list.append((img, img_rect, "ground"))
                if tile == 2:
                    img = pygame.transform.scale(ground_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    self.tile_list.append((img, img_rect, "ground"))
                if tile == 3:
                    img = pygame.transform.scale(spike_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    self.tile_list.append((img, img_rect, "trap"))

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            SCREEN.blit(tile[0], tile[1])
            #pygame.draw.rect(SCREEN, (255, 255, 255), tile[1], 1)


class Game:
    def __init__(self, start_scene):
        self.scene = start_scene

    def run(self):
        run = True
        clock = pg.time.Clock()
        while run:
            clock.tick(FPS)

            next_scene = self.scene.update()
            if next_scene:
                self.scene = next_scene
            self.scene.draw()
            #self.scene.player.draw()

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
        self.player = Player(player_pos[0], player_pos[1], True)

    def draw(self):
        self.world.draw()

class Level5(Level_scene):
    def __init__(self):
        super().__init__(world_data_5, START_POS)

    def update(self):
        self.player.update(self.world)

        if self.player.rect.x > WIDTH:
            pass
            # return Level3()
    def draw(self):
        SCREEN.blit(bg_img_level5, (0, 0))
        self.player.draw()
        return super().draw()


class Level4(Level_scene):
    def __init__(self):
        super().__init__(world_data_4, START_POS)

    def update(self):
        self.player.update(self.world)

        if self.player.rect.x > WIDTH:
            return Level5()

    def draw(self):
        SCREEN.blit(bg_img_level4, (0, 0))
        self.player.draw()
        return super().draw()

class Level3(Level_scene):
    def __init__(self):
        super().__init__(world_data_3, START_POS_3)

    def update(self):
        self.player.update(self.world)

        if self.player.rect.x > WIDTH:
            return Level4()
    def draw(self):
        SCREEN.blit(bg_img_level3, (0, 0))
        self.player.draw()
        return super().draw()


class Level2_5(Level_scene):
    def __init__(self):
        super().__init__(world_data_2_5, START_POS_2_5)

    def update(self):
        self.player.update(self.world)

        if self.player.rect.y > HEIGHT:
            return Level4()
    def draw(self):
        SCREEN.blit(bg_img_level2_5, (0, 0))
        self.player.draw()
        return super().draw()


class Level2(Level_scene):
    def __init__(self):
        super().__init__(world_data_2, START_POS_2)

    def update(self):
        self.player.update(self.world)

        if self.player.rect.x > WIDTH:
            return Level3()
    def draw(self):
        SCREEN.blit(bg_img_level2, (0, 0))
        self.player.draw()
        return super().draw()


class Level1(Level_scene):
    def __init__(self):
        super().__init__(world_data_1, START_POS_1)

    def update(self):
        self.player.update(self.world)

        if self.player.rect.y > HEIGHT:
            return Level2()
        if self.player.rect.x > WIDTH:
            return Level2_5()


    def draw(self):
        SCREEN.blit(bg_img, (0, 0))
        self.player.draw()
        return super().draw()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    return textrect


class Start_screen(Scene):
    picture1_img = pygame.image.load("assets/img/normal_mode.png").convert_alpha()
    picture2_img = pygame.image.load("assets/img/last_chance_mode.png").convert_alpha()
    picture1_hover_img = pygame.image.load("assets/img/normal_mode_hover.png").convert_alpha()
    picture2_hover_img = pygame.image.load("assets/img/last_chance_mode_hover.png").convert_alpha()

    # Juster størrelsen på bildene
    button_width = 500
    button_height = 300
    picture1_img = pygame.transform.scale(picture1_img, (button_width, button_height))
    picture2_img = pygame.transform.scale(picture2_img, (button_width, button_height))
    picture1_hover_img = pygame.transform.scale(picture1_hover_img, (button_width, button_height))
    picture2_hover_img = pygame.transform.scale(picture2_hover_img, (button_width, button_height))

    # Posisjoner for knappene
    button_spacing = 60
    button_y = (HEIGHT - button_height) // 2
    picture1_x = (WIDTH - button_width * 2 - button_spacing) // 2
    picture2_x = picture1_x + button_width + button_spacing

    running = True

    def update(self):
        SCREEN.fill(START_COLOR)
        draw_text("Velg vanskelighetsgrad:", font, WHITE, SCREEN, WIDTH // 2, HEIGHT // 6)

        # Tegn standardbilder
        SCREEN.blit(self.picture1_img, (self.picture1_x, self.button_y))
        SCREEN.blit(self.picture2_img, (self.picture2_x, self.button_y))

        # Hent museposisjonen
        mouse_pos = pygame.mouse.get_pos()

        # Sjekk for hover-effekt og tegn hover-bilder
        if self.picture1_img.get_rect(topleft=(self.picture1_x, self.button_y)).collidepoint(mouse_pos):
            SCREEN.blit(self.picture1_hover_img, (self.picture1_x, self.button_y))
        if self.picture2_img.get_rect(topleft=(self.picture2_x, self.button_y)).collidepoint(mouse_pos):
            SCREEN.blit(self.picture2_hover_img, (self.picture2_x, self.button_y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.picture1_img.get_rect(topleft=(self.picture1_x, self.button_y)).collidepoint(mouse_pos):
                    # Start hovedspillet med 1 liv
                    return Level1()

                elif self.picture2_img.get_rect(topleft=(self.picture2_x, self.button_y)).collidepoint(mouse_pos):
                    # Start hovedspillet med 2 liv
                    return Level1()


game = Game(Start_screen())
game.run()

pygame.quit()
