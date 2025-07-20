import pygame
from pygame import *
from random import randint
from time import time as timer

win_width = 1300
win_height = 700
window = display.set_mode((win_width, win_height))

display.set_caption('Shooter')
#display.set_icon()

background = transform.scale(image.load('background.jpg'), (win_width, win_height))
clock = pygame.time.Clock()

mixer.init()
mixer.music.load('music.ogg')
mixer.music.set_volume(.5)
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.Font(None, 36)
font1 = font.Font(None, 80)

lost = 0
score = 0
max_lost = 3
max_win = 25

life = 3
life_color = (0, 0, 0)

num_fire = 10
rel_time = False
last_time = False

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, width, height, speed, img):
        sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > -25:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 75:
            self.rect.x += self.speed

    def fire(self):
        b = Bullet(self.rect.centerx, self.rect.top, 15, 40, 15, 'bullet.png')
        bullets.add(b)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player(500, 600, 170, 120, 25, 'rocket.png')

run = True
finish = False

monsters = sprite.Group()
for i in range(5):
    mnst = Enemy(randint(80, win_width-80), randint(175, 300), 70, 70, 2, 'monster.png')
    monsters.add(mnst)

asteroids = sprite.Group()
for i in range(3):
    ast = Enemy(randint(30, win_width-30), -40, 70, 70, 3, 'asteroid.png')
    asteroids.add(ast)

bullets = sprite.Group()

while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if num_fire > 0 and not rel_time:
                    num_fire -= 1
                    fire_sound.play()
                    player.fire()
                if num_fire <= 0 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))

        text_score = font2.render('Рахунок: ' + str(score), True, (107, 255, 127))
        window.blit(text_score, (10, 20))

        text_lost = font2.render('Пропущено: ' + str(lost), True, (255, 127, 107))
        window.blit(text_lost, (10, 70))

        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('wait, reloading...', True, (170, 0, 0))
                window.blit(reload, (260, 460))
            else:
                rel_time = False
                num_fire = 10

        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(bullets, monsters, True, True)
        for c in collides:
            score += 1
            m = Enemy(randint(80, win_width-80), randint(175, 300), 70, 70, 2, 'monster.png')
            monsters.add(m)

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            life -= 1
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)

        if lost >= max_lost or life <= 0:
            finish = True
            lose_text = font1.render('YOU LOSE', True, (255, 0, 0))
            window.blit(lose_text, (200, 200))

        if score >= max_win:
            finish = True
            win_text = font1.render('YOU WIN', True, (0, 255, 0))
            window.blit(win_text, (200, 200))

        if life == 3:
            life_color = (0, 255, 0)
        if life == 2:
            life_color = (255, 255, 0)
        if life == 1:
            life_color = (255, 0, 0)
        text_life = font1.render(str(life), True, life_color)
        window.blit(text_life, (win_width-100, 20))

        display.update()
    time.delay(50)