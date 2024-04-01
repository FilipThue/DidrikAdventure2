# Tutorial for å forstå tiles: https://www.youtube.com/watch?v=Ongc4EVqRjo

import pygame
from settings import *
from sprites import *

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
    def __init__(self, data, lives):
        self.tile_list = []
        self.lives = lives

        self.checkpoint_life_img = py.transform.scale(checkpoint_life_img, (16 * LIFE_SCALE, 10 * LIFE_SCALE))
        self.one_life_img = py.transform.scale(one_life_img, (16 * LIFE_SCALE, 10 * LIFE_SCALE))

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

    def update(self):
        if self.lives < 0:
            print("Du er død")

    def draw(self):
        for tile in self.tile_list:
            SCREEN.blit(tile[0], tile[1])
            # pygame.draw.rect(SCREEN, (255, 255, 255), tile[1], 1)
        if self.lives > 0:
            SCREEN.blit(self.checkpoint_life_img, LIFE_POSITION)
        if self.lives == 0:
            SCREEN.blit(self.one_life_img, LIFE_POSITION)


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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()


#/------------------------------------------------------

class Prop:
    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = pygame.transform.scale(img, (w, h))

    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))



class Spike:
    def __init__(self, x, y):
        self.img = pygame.transform.scale(spike_img, (TILE_SIZE, TILE_SIZE))
        self.x = x
        self.y = y
        self.hitbox = [x + SPIKE_LENIENCY / 2, y + SPIKE_LENIENCY, TILE_SIZE - SPIKE_LENIENCY,
                       TILE_SIZE - SPIKE_LENIENCY]

    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))
        pygame.draw.rect(SCREEN, RED, self.hitbox, 2)


#/------------------------------------------------------


class Scene:
    def update(self):
        return self

    def draw(self):
        pass


class Level_scene(Scene):
    def __init__(self, world_d, player_pos, lives):
        self.world = World(world_d, lives)
        self.player = Player(player_pos[0], player_pos[1])
        self.lives = lives

    def common_update(self):
        self.world.update()
        self.player.update(self.world)

    def draw(self):
        self.world.draw()


class Level5(Level_scene):
    def __init__(self, lives):
        super().__init__(world_data_5, START_POS, lives)

    def update(self):
        self.common_update()

        if self.player.rect.x > WIDTH:
            pass
            # return Level3()

    def draw(self):
        SCREEN.blit(bg_img_level5, (0, 0))
        self.player.draw()
        return super().draw()


class Level4(Level_scene):
    def __init__(self, lives):
        super().__init__(world_data_4, START_POS, lives)

    def update(self):
        self.common_update()

        if self.player.rect.x > WIDTH:
            return Level5(self.lives)

    def draw(self):
        SCREEN.blit(bg_img_level4, (0, 0))
        self.player.draw()
        return super().draw()


class Level3(Level_scene):
    def __init__(self, lives):
        super().__init__(world_data_3, START_POS, lives)
        self.spike = Spike(-1 * TILE_SIZE, 12 * TILE_SIZE)
        self.homing_spike = False

    def update(self):
        self.common_update()

        if self.player.vel_y < 0:
            self.homing_spike = True

        if self.player.rect.x > 700:
            self.homing_spike = True

        if self.homing_spike:
            if self.spike.hitbox[0] < self.player.rect.x:
                if self.player.rect.x - self.spike.hitbox[0] < 60:
                    self.spike.hitbox[0] += WALKING_SPEED
                    self.spike.x += WALKING_SPEED
                else:
                    self.spike.hitbox[0] += SPIKE_SPEED * 3
                    self.spike.x += SPIKE_SPEED * 3

        if self.player.rect.colliderect(self.spike.hitbox):
            if self.lives == 1:
                return Level3(self.lives)
            else:
                return Start_screen()

        if self.player.rect.x > WIDTH:
            return Level4(self.lives)

    def draw(self):
        SCREEN.blit(bg_img_level3, (0, 0))
        self.player.draw()
        self.spike.draw()
        return super().draw()


class Level2_5(Level_scene):
    def __init__(self, lives):
        super().__init__(world_data_2_5, START_POS, lives)

    def update(self):
        self.common_update()

        if self.player.rect.y > HEIGHT:
            return Level4(self.lives)

    def draw(self):
        SCREEN.blit(bg_img_level2_5, (0, 0))
        self.player.draw()
        return super().draw()


class Level2(Level_scene):
    def __init__(self, lives):
        super().__init__(world_data_2, START_POS_2, lives)
        self.portals = [Portal(280, 90), Portal(770, 90)]
        self.level_started = 0
        self.trap_activation = 5 * TILE_SIZE
        self.spikes = [Spike(8 * TILE_SIZE, 8 * TILE_SIZE), Spike(19 * TILE_SIZE, 9 * TILE_SIZE), Spike(9 * TILE_SIZE, 4 * TILE_SIZE), Spike(10 * TILE_SIZE, 13 * TILE_SIZE)]
        for i in range(6):
            self.spikes.append(Spike((12 + i) * TILE_SIZE, 13 * TILE_SIZE))
        self.trap_timer = 0
        self.trap_activated = False


    def update(self):
        self.common_update()
        for i in range(2):
            self.portals[i].update_sprite()


        # feller
        if self.player.rect.x > self.trap_activation - self.player.width:
            self.level_started += 1

        if self.level_started == 1:
            self.spikes.insert(0, Spike(self.trap_activation, 11 * TILE_SIZE))
            self.trap_activated = True

        if self.trap_timer > 90:
            if self.trap_activated:
                self.trap_activated = False
                if len(self.spikes) > 10:
                    self.spikes.pop(3)
                self.trap_timer = 0
            else:
                self.trap_activated = True
                if len(self.spikes) < 11:
                    self.spikes.insert(3, Spike(9 * TILE_SIZE, 4 * TILE_SIZE))
                self.trap_timer = 0

        if self.player.rect.x > 21 * TILE_SIZE:
            if self.spikes[2].hitbox[0] < self.player.rect.x:
                self.spikes[2].hitbox[0] += SPIKE_SPEED
                self.spikes[2].x += SPIKE_SPEED



        for i in range(len(self.spikes)):
            if self.player.rect.colliderect(self.spikes[i].hitbox):
                if self.lives == 1:
                    return Level2(self.lives)
                else:
                    return Start_screen()

        # portalen
        if 280 < self.player.rect.x < 300 and 90 < self.player.rect.y < 200:  # definerer portalinngangen
            self.player.rect.x = 800


        if self.player.rect.x > WIDTH:
            return Level3(self.lives)

        self.trap_timer += 1

    def draw(self):
        SCREEN.blit(bg_img_level2, (0, 0))

        for i in range(2):
            self.portals[i].draw()

        self.player.draw()

        for i in range(len(self.spikes)):
            self.spikes[i].draw()

        return super().draw()



class Level1(Level_scene):
    def __init__(self, lives):
        super().__init__(world_data_1, START_POS, lives)
        self.hidden_tile_x = 17 * TILE_SIZE
        self.props = []
        self.spike = Spike(13 * TILE_SIZE, 12 * TILE_SIZE)
        for i in range (3):
            self.props.append(Prop(self.hidden_tile_x + TILE_SIZE * i, HEIGHT-TILE_SIZE, TILE_SIZE, TILE_SIZE, ground_img))


    def update(self):
        self.common_update()

        if self.player.rect.colliderect(self.spike.hitbox):
            if self.lives == 1:
                return Level1(self.lives)
            else:
                return Start_screen()


        if self.player.rect.y > HEIGHT:
            return Level2(self.lives)
        if self.player.rect.x > WIDTH:
            return Level2_5(self.lives)

    def draw(self):
        SCREEN.blit(bg_img, (0, 0))

        if self.player.rect.x < self.hidden_tile_x:
            for i in range(len(self.props)):
                self.props[i].draw()

        self.player.draw()
        self.spike.draw()
        return super().draw()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    return textrect


class Start_screen(Scene):
    last_chance_mode_img = pygame.image.load("assets/img/last_chance_mode.png").convert_alpha()
    normal_mode_img = pygame.image.load("assets/img/normal_mode.png").convert_alpha()
    last_chance_mode_hover_img = pygame.image.load("assets/img/last_chance_mode_hover.png").convert_alpha()
    normal_mode_hover_img = pygame.image.load("assets/img/normal_mode_hover.png").convert_alpha()

    # Juster størrelsen på bildene
    last_chance_mode_img = pygame.transform.scale(last_chance_mode_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
    normal_mode_img = pygame.transform.scale(normal_mode_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
    last_chance_mode_hover_img = pygame.transform.scale(last_chance_mode_hover_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
    normal_mode_hover_img = pygame.transform.scale(normal_mode_hover_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    # Posisjoner for knappene
    normal_mode_img_x = (WIDTH - BUTTON_WIDTH * 2 - BUTTON_SPACING) // 2
    last_chance_mode_img_x = normal_mode_img_x + BUTTON_WIDTH + BUTTON_SPACING

    running = True

    def update(self):
        SCREEN.fill(START_COLOR)
        draw_text("Velg vanskelighetsgrad:", font, WHITE, SCREEN, WIDTH // 2, HEIGHT // 6)

        # Tegn standardbilder
        SCREEN.blit(self.normal_mode_img, (self.last_chance_mode_img_x, BUTTON_y))
        SCREEN.blit(self.last_chance_mode_img, (self.normal_mode_img_x, BUTTON_y))

        # Hent museposisjonen
        mouse_pos = pygame.mouse.get_pos()

        # Sjekk for hover-effekt og tegn hover-bilder
        if self.normal_mode_img.get_rect(topleft=(self.last_chance_mode_img_x, BUTTON_y)).collidepoint(mouse_pos):
            SCREEN.blit(self.normal_mode_hover_img, (self.last_chance_mode_img_x, BUTTON_y))
        if self.last_chance_mode_img.get_rect(topleft=(self.normal_mode_img_x, BUTTON_y)).collidepoint(mouse_pos):
            SCREEN.blit(self.last_chance_mode_hover_img, (self.normal_mode_img_x, BUTTON_y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.last_chance_mode_img.get_rect(topleft=(self.normal_mode_img_x, BUTTON_y)).collidepoint(
                        mouse_pos):
                    # Start hovedspillet med 1 liv
                    return Level1(0)

                elif self.normal_mode_img.get_rect(topleft=(self.last_chance_mode_img_x, BUTTON_y)).collidepoint(
                        mouse_pos):
                    # Start hovedspillet med 5 liv
                    return Level1(1)


game = Game(Start_screen())
game.run()

pygame.quit()


