#!/usr/bin/env python

import math
import sys
from random import randint

from serial import Serial
from serial.tools import list_ports
import pygame


class SpaceShip(object):
    def __init__(self, img, pos=[100, 100], size=[50, 75]):
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, size)
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.vel, self.avel = [0, 0], 0
        self.angle = 0

        self.health, self.max_health = 100, 100
        self.bvel = 10


class UFO(SpaceShip):
    def __init__(self, img, pos=[100, 500], size=[120, 70]):
        super(self.__class__, self).__init__(img, pos, size)
        self.fire_rate, self.inacc = 50, 30

    def move(self):
        self.rect = self.rect.move(*self.vel)
        if (self.rect.left < 0) or (self.rect.right > w):
            self.vel[0] = -self.vel[0]
        if (self.rect.top < 0) or (self.rect.bottom > h):
            self.vel[1] = -self.vel[1]

    def fire(self, scenter):
        if (ticks % self.fire_rate) != 0:
            return
        oopsx = randint(-self.inacc, self.inacc)
        oopsy = randint(-self.inacc, self.inacc)

        ufo_x, ufo_y = self.rect.center
        dx, dy = scenter[0] - ufo_x + oopsx, ufo_y - scenter[1] + oopsy
        angle = math.atan2(dx, dy)

        bx_vel = self.bvel * math.sin(angle)
        by_vel = -self.bvel * math.cos(angle)
        b_vel = [bx_vel, by_vel]

        b = Bullet(self.rect.center, b_vel, color=(0, 200, 0))
        bullets.append(b)
        ufo_laser.play()


class Bullet(object):
    def __init__(self, pos, vel, size=[15, 15], color=(200, 0, 0)):
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.vel = vel
        self.color = color

        self.damage, self.enemy = 5, True


def joystick_angle(x, y):
    x, y = x - 512, -y + 512
    if (abs(x) > 20) or (abs(y) > 20):  # Movement
        return math.degrees(math.atan2(x, y))


ports = [p for p in list_ports.grep(sys.argv[1])]
if not ports:
    raise IOError("Port " + sys.argv[1] + " not found!")
else:
    serial = Serial(ports[0][0], 19200)

pygame.init()

info = pygame.display.Info()
size = w, h = info.current_w, info.current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("Ship Mover")
srect = screen.get_rect()

pygame.mouse.set_visible(0)

ship = SpaceShip("resources/img/ship.png")
enemies = []

ship_laser = pygame.mixer.Sound("resources/sound/laser.ogg")
ship_laser.set_volume(0.25)
ufo_laser = pygame.mixer.Sound("resources/sound/ulaser.ogg")
ship_laser.set_volume(0.5)
hitsound = pygame.mixer.Sound("resources/sound/hit.ogg")
hitsound.set_volume(0.25)
boom = pygame.mixer.Sound("resources/sound/explosion.ogg")
pygame.mixer.music.load("resources/sound/space.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

bullets = []
hits, shots = 0, 0
can_fire = False  # Cannot press and hold fire
score, wave = 0, 0

dfont = pygame.font.Font("resources/fonts/mc.ttf", 24)

clock = pygame.time.Clock()
ticks = 0
while True:
    ## WAVES ###
    if not enemies and ship.health > 0:
        wave += 1
        ship.health = 100
        score += (wave - 1) * 100

        vbound = min(5, wave / 2)
        frate = 100 - wave + (wave / 100) + 1
        inacc = max(0, 30 - wave)
        for _ in xrange(wave / 5 + 1):
            pos = [randint(0, w), randint(0, h)]
            v = [randint(-vbound, vbound), randint(-vbound, vbound)]
            ufo = UFO("resources/img/ufo.png", pos)
            ufo.rect = ufo.rect.clamp(srect)
            ufo.vel, ufo.fire_rate, ufo.inacc = v, frate, inacc
            enemies.append(ufo)

    ### CONTROLLER ###

    try:
        joy = [int(n) for n in serial.readline().split()]
        assert len(joy) == 3
    except:
        joy = [512, 512, 0]
    angle = joystick_angle(joy[0], joy[1])

    if angle is not None:
        ship.avel = 5
        ship.angle = -angle
    else:
        ship.avel = 0

    if joy[2] and can_fire:
        bx_vel = ship.bvel * math.sin(math.radians(-ship.angle))
        by_vel = -ship.bvel * math.cos(math.radians(ship.angle))

        b_vel = map(sum, zip([bx_vel, by_vel], ship.vel))
        b = Bullet(ship.rect.center, b_vel)
        b.enemy = False
        bullets.append(b)
        ship_laser.play()
        shots += 1
        can_fire = False

    if not joy[2]:
        can_fire = True

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)

    ### MOVEMENT ###

    for bullet in bullets:
        bullet.rect = bullet.rect.move(*bullet.vel)

    rotufo = pygame.transform.rotate(ship.img, ship.angle)
    rotrect = rotufo.get_rect()
    rotrect.center = ship.rect.center

    x_vel = ship.avel * math.sin(math.radians(-ship.angle))
    y_vel = -ship.avel * math.cos(math.radians(ship.angle))
    ship.vel = [x_vel, y_vel]

    ship.rect = ship.rect.move(*ship.vel)
    ship.rect = ship.rect.clamp(srect)

    for enemy in enemies:
        enemy.fire(ship.rect.center)
        enemy.move()

    ### COLLISION ###
    del_bullets = []

    hit = ship.rect.collidelistall(bullets)
    for b in hit:
        bullet = bullets[b]
        if bullet.enemy and ship.health > 0:
            del_bullets.append(bullet)
            ship.health -= bullet.damage
            score = max(0, score - bullet.damage)
            hitsound.play()
            if ship.health <= 0:
                pygame.mixer.music.fadeout(15000)
                enemies = []
                ship.img = pygame.image.load("resources/img/null.png")

    for enemy in enemies:
        hit = enemy.rect.collidelistall(bullets)
        for b in hit:
            bullet = bullets[b]
            if not bullet.enemy:
                del_bullets.append(bullet)
                enemy.health -= bullet.damage
                hits += 1
                score += bullet.damage
                hitsound.play()
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    boom.play()

    bullets = [b for b in bullets if b not in del_bullets]

    ### DRAWING ###

    screen.fill((0, 0, 0))

    screen.blit(rotufo, rotrect)

    for enemy in enemies:
        er = enemy.rect
        hw = (float(enemy.health) / enemy.max_health) * er.width
        hrect = pygame.Rect(er.left, er.top - 10, hw, 5)
        pygame.draw.rect(screen, (0, 200, 0), hrect)
        screen.blit(enemy.img, enemy.rect)

    for bullet in bullets:
        rad = bullet.rect.width / 2
        if not srect.contains(bullet.rect):  # Bullet off-screen
            bullets.remove(bullet)
        pygame.draw.circle(screen, bullet.color, bullet.rect.center, rad)

    hp = "HP: {0}/{1}".format(ship.health, ship.max_health)
    health = dfont.render(hp, 1, (255, 0, 0))
    hrect = health.get_rect()
    hrect.right = w - 20
    screen.blit(health, hrect)

    if shots:
        p = round(100 * (float(hits) / shots), 1)
    else:
        p = "---.-"
    acc = "ACC: {0}%".format(p)
    accuracy = dfont.render(acc, 1, (0, 255, 0))
    arect = accuracy.get_rect()
    arect.topright = [w - 20, 30]
    screen.blit(accuracy, arect)

    sc = "SCORE: {0}".format(score)
    stext = dfont.render(sc, 1, (255, 255, 50))
    screct = stext.get_rect()
    screct.left = 10
    screen.blit(stext, screct)

    wv = "WAVE {0}".format(wave)
    wtext = dfont.render(wv, 1, (255, 125, 0))
    wrect = wtext.get_rect()
    wrect.topright = [w - 20, 65]
    screen.blit(wtext, wrect)

    if ship.health <= 0:
        endtext = "GAME OVER"
        end = dfont.render(endtext, 1, (255, 255, 255))
        endrect = pygame.Rect((0, 0), end.get_rect().size)
        endrect.center = srect.center
        screen.blit(end, endrect)
        can_fire = False

    pygame.display.flip()

    clock.tick(200)
    ticks += 1
