import pygame, sys
from player import Player
import obstacles
from enemy import Enemy, Extra
from random import choice, randint
from laser import Laser

class Game:
    def __init__(self):
        player_sprite = Player((screen_width/2, screen_height), screen_width, 6)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.lives = 4
        self.live_surf = pygame.image.load('./img/Hpcount1.gif').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 3 + 20)

        self.score = 0
        self.font = pygame.font.Font('./img/font.ttf', 20)

        self.shape = obstacles.shape
        self.block_size = 6
        self.block = pygame.sprite.Group()
        self.obstacle_amount = 8
        self.obstacle_pos = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacle(0, 100, 200, 300, 400, 500, 600, 700, x_start = 0, y_start = 880)
        self.extra = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.Group()
        self.enemy_setup(rows=6, cols=8, x_distance=60, y_distance=48, x_offset=60, y_offset=90)
        self.enemy_direction = 1
        self.enemy_lasers = pygame.sprite.Group()
        self.extra_spawn_time = randint(40, 80)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start+col_index * self.block_size + offset_x
                    y = y_start+row_index * self.block_size
                    block = obstacles.Block(self.block_size, (241, 79, 80), x, y)
                    self.block.add(block)
    def create_multiple_obstacle(self, *offset, x_start, y_start):
        for x in offset:
            self.create_obstacle(x_start, y_start, x)
    def enemy_setup(self, rows, cols, x_distance, y_distance, x_offset, y_offset):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    enemy_sprite = Enemy('enemy6', x, y)
                elif 1 <= row_index <= 2:
                    enemy_sprite = Enemy('enemy4', x, y)
                elif 3 <= row_index <= 4:
                    enemy_sprite = Enemy('enemy2', x, y)
                elif 5 <= row_index <= 6:
                    enemy_sprite = Enemy('enemy3', x, y)
                else:
                    enemy_sprite = Enemy('enemy4', x, y)
                self.enemy.add(enemy_sprite)
    def enemy_pos_checker(self):
        all_enemys = self.enemy.sprites()
        for enemy in all_enemys:
            if enemy.rect.right >= screen_width:
                self.enemy_direction = -1
                self.enemy_move_down(1)
            elif enemy.rect.left <= 0:
                self.enemy_direction = 1
                self.enemy_move_down(1)

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * self.live_surf.get_size()[0] + 10)
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (10, 10))
        screen.blit(score_surf, score_rect)

    def enemy_shoot(self):
        if self.enemy.sprites():
            random_enemy = choice(self.enemy.sprites())
            laser_sprite = Laser(random_enemy.rect.center, screen_height, 6)
            self.enemy_lasers.add(laser_sprite)
    def enemy_move_down(self, distance):
        if self.enemy:
            for enemy in self.enemy.sprites():
                enemy.rect.y += distance
    
    def collision_checks(self):
        if self.player.sprite.layer:
            for laser in self.player.sprite.layer:
                if pygame.sprite.spritecollide(laser, self.block, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.enemy, True):
                    laser.kill()
                    self.score += 250


                if pygame.sprite.spritecollide(laser, self.extra, True):
                    laser.kill()
                    self.score += 500
        if self.enemy_lasers:
            for laser in self.enemy_lasers:
                if pygame.sprite.spritecollide(laser, self.block, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.enemy:
            for enemys in self.enemy:
                pygame.sprite.spritecollide(enemys, self.player, True)
                if pygame.sprite.spritecollide(enemys, self.player, False):
                    pygame.quit()
                    sys.exit()

    def extra_enemy_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 800)

    def victory_message(self):
        if not self.enemy.sprites():
            victory_surf = self.font.render('you won', False, 'white')
            victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(victory_surf, victory_rect)


    def run(self):
        self.display_lives()
        self.display_score()
        self.player.sprite.layer.draw(screen)
        self.player.update()
        self.enemy.update(self.enemy_direction)
        self.enemy_pos_checker()
        self.enemy_lasers.update()
        self.player.draw(screen)
        self.enemy.draw(screen)
        self.block.draw(screen)
        self.enemy_lasers.draw(screen)
        self.extra_enemy_timer()
        self.extra.draw(screen)
        self.extra.update()
        self.collision_checks()
        self.victory_message()

pygame.init()
screen_width = 800
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

ENEMYLASER = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMYLASER, 900)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == ENEMYLASER:
            game.enemy_shoot()
    screen.fill((30, 30, 30))
    game.run()
    pygame.display.flip()
    clock.tick(60)