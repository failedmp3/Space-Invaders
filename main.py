import pygame
import time
from random import randint

pygame.mixer.init()
pygame.mixer.music.load('assets/space.ogg')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)
fire_sound = pygame.mixer.Sound('assets/fire.ogg')

win_width = 700
win_height = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Space Shooter')
background = pygame.transform.scale(
    pygame.image.load('assets/galaxy.jpg'), (win_width, win_height))
clock = pygame.time.Clock()

game = True
finish = False
paused = False

MIN_ENEMY_SPEED = 1
MAX_ENEMY_SPEED = 4

score = 0
missed = 0

pygame.font.init()
font = pygame.font.Font(None, 36)
font_big = pygame.font.Font(None, 72)

win_text = font_big.render("You Win! 0o0", True, (50, 255, 50))
lose_text = font_big.render('You Lose! T-T', True, (255, 0, 0))
pause_text = font_big.render("Paused", True, (255, 255, 255))

last_time_fire = time.time()


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_image, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(sprite_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < win_width-self.rect.width:
            self.rect.x += self.speed

    def fire(self):
        global last_time_fire
        cur_time_fire = time.time()
        if cur_time_fire - last_time_fire > 0.3:
            bullet = Bullet('assets/bullet.png', self.rect.centerx,
                            self.rect.top, 10,20,15)
            bullets.add(bullet)
            fire_sound.play()
            last_time_fire = cur_time_fire


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > win_height:
            self.rect.x = randint(5, win_width - self.rect.width)
            self.speed = randint(MIN_ENEMY_SPEED, MAX_ENEMY_SPEED)
            self.rect.y = -60
            missed += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -50:
            self.kill()

player = Player('assets/rocket.png', 200, win_height-100, 50, 80, 10)

aliens = pygame.sprite.Group()
for i in range(6):
    x = randint(5, win_width - 120)
    y = 40
    speed = randint(MIN_ENEMY_SPEED, MAX_ENEMY_SPEED)
    alien = Enemy('assets/ufo.png', x, y, 90, 60, speed)
    aliens.add(alien)


bullets = pygame.sprite.Group()
paused_surface = pygame.Surface((win_width, win_height), pygame.SRCALPHA)
paused_color = (70, 40, 110, 128)
paused_surface.fill(paused_color)


while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not finish:
                player.fire()
            if event.key == pygame.K_ESCAPE:
                if paused:
                    paused = False
                else:
                    paused = True

    if paused:
        window.blit(background, (0, 0))
        player.reset()
        aliens.draw(window)
        bullets.draw(window)
        window.blit(paused_surface, (0, 0))
        pygame.display.update()




    if not finish and not paused:
        window.blit(background, (0, 0))


        player.update()
        player.reset()

        aliens.update()
        aliens.draw(window)

        bullets.update()
        bullets.draw(window)

        score_label = font.render(f"Score: {score}", True, (255, 255, 255))
        missed_label = font.render(f"Missed: {missed}", True, (255, 255, 255))

        window.blit(score_label, (10, 20))
        window.blit(missed_label, (10, 50))

        collides = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for c in collides:
            score += 1
            x = randint(5, win_width - 120)
            y = 40
            speed = randint(MIN_ENEMY_SPEED, MAX_ENEMY_SPEED)
            alien = Enemy('assets/ufo.png', x, y, 90, 60, speed)
            aliens.add(alien)

        if pygame.sprite.spritecollide(player, aliens, False) or missed > 10:
            finish = True
            window.blit(lose_text, (200, 250))

        if score > 29:
            finish = True
            window.blit(win_text, (200, 250))


        pygame.display.update()

    clock.tick(60)