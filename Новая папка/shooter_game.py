#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer
lost = 0
life = 5
max_bullets = 30
num_bullet = 0  
reload_bullets = False
score = 0 
max_lost = 6 
max_score = 15

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def recet(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed [K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed  
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 1 )
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost  
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = -50
            lost += 1

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()




 
rocket = Player('yellow_soull.png', 300, 400, 5)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('attack.png', randint(0, 700 - 80), -40, 1)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(2):
    asteroid = Enemy('asteroid.png', randint(0, 700 - 80), -40, 1)
    asteroids.add(asteroid)


window = display.set_mode((700, 500))
display.set_caption("pygame window")
background = transform.scale(image.load("mettaton_ex.jpg"), (700, 500))

clock = time.Clock()
FPS = 60

clock.tick(FPS)

mixer.init()
mixer.music.load('Toby_Fox_-_Death_By_Glamour_64962823.ogg')
bullet_sound = mixer.Sound('fire.ogg')
mixer.music.play()

bullets = sprite.Group()

font.init()
font = font.SysFont('Arial', 36)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

game = True 
while game:
    window.blit(background,(0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_bullet < max_bullets and reload_bullets == False:
                    rocket.fire()
                    num_bullet += 1 
                if num_bullet >= max_bullets and reload_bullets == False:
                    reload_bullets = False
        if sprite.groupcollide(monsters, bullets, True, True):
            score += 1
            game = True
            monster = Enemy('attack.png', randint(0, 700 - 80), -40, 1)
            monsters.add(monster)
        if sprite.spritecollide(rocket, monsters, False) or sprite.spritecollide(rocket, asteroids, False):
            sprite.spritecollide(rocket, monsters, True)
            sprite.spritecollide(rocket, asteroids, True)
            life -= 1 
            window.blit(lose, (200, 200))
        if score >= max_score:
            game = False 
            window.blit(win, (200, 200))
        if life == 0 or lost >= max_lost:
            game = False
            window.blit(lose, (200, 200))


    rocket.recet()
    rocket.update() 
    bullets.update()
    asteroids.update()
    monsters.update()
    asteroids.draw(window)
    monsters.draw(window)
    bullets.draw(window)
    display.update() 



